const test = require('node:test');
const assert = require('node:assert/strict');
const { spawn, spawnSync } = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const crypto = require('node:crypto');

const ROOT = path.join(__dirname, '..');
const KEY = crypto.randomBytes(32).toString('hex');
const tmp = () => fs.mkdtempSync(path.join(os.tmpdir(), 'acosta-'));

// ---------- almacén cifrado ----------
const storeLib = require('../src/store');

test('almacén: cifra en disco, no deja datos en claro y se recupera con la clave', () => {
  const dir = tmp();
  const s = storeLib.open({ dir, keyHex: KEY });
  const r = s.append({ nombre: 'María Pérez', telefono: '612345678', estado: 'pendiente' });
  const raw = fs.readFileSync(path.join(dir, 'solicitudes.enc'), 'utf8');
  assert.ok(!raw.includes('María') && !raw.includes('612345678'), 'el archivo no debe contener datos en claro');
  assert.equal(storeLib.open({ dir, keyHex: KEY }).get(r.id).telefono, '612345678');
});

test('almacén: con otra clave o archivo manipulado falla (no devuelve datos)', () => {
  const dir = tmp();
  storeLib.open({ dir, keyHex: KEY }).append({ nombre: 'X', estado: 'pendiente' });
  assert.throws(() => storeLib.open({ dir, keyHex: crypto.randomBytes(32).toString('hex') }));
  const f = path.join(dir, 'solicitudes.enc');
  const b = Buffer.from(fs.readFileSync(f, 'utf8').trim(), 'base64'); b[40] ^= 1;
  fs.writeFileSync(f, b.toString('base64'));
  assert.throws(() => storeLib.open({ dir, keyHex: KEY }));
});

test('almacén: la retención borra lo antiguo pero nunca lo pendiente', () => {
  const s = storeLib.open();
  const old = new Date(Date.now() - 400 * 86_400_000).toISOString();
  s.append({ creada: old, estado: 'respondida' }); s.append({ creada: old, estado: 'pendiente' }); s.append({ estado: 'respondida' });
  assert.equal(s.purge(12), 1);
  assert.equal(s.all().length, 2);
});

// ---------- avisos ----------
test('avisos: nunca incluyen datos personales', async () => {
  const { notify } = require('../src/notify');
  const calls = [];
  const orig = global.fetch;
  global.fetch = async (url, init) => { calls.push({ url, init }); return { ok: true }; };
  try {
    const r = await notify({ id: 'W-1', tipo: 'apertura', municipio: 'El Paso', urgente: true, nombre: 'María', telefono: '612345678' }, { NTFY_TOPIC: 'tema-secreto', TELEGRAM_BOT_TOKEN: 'tok', TELEGRAM_CHAT_ID: '1' });
    assert.equal(r.sent, 2);
    const todo = JSON.stringify(calls);
    assert.ok(!/María|612345678/.test(todo));
    assert.match(r.texto, /URGENTE.*apertura de puerta.*El Paso/);
  } finally { global.fetch = orig; }
});

// ---------- formulario + almacén + recuperación tras reinicio ----------
test('formulario: guarda cifrado, avisa, y recupera pendientes tras reiniciar', async () => {
  const contact = require('../src/contact');
  const dir = tmp();
  const avisos = [];
  contact.configure({ store: storeLib.open({ dir, keyHex: KEY }), notify: async (a) => { avisos.push(a); } });
  const r = contact.submit({ nombre: 'Juan Ramón', telefono: '669 76 86 59', municipio: 'El Paso', tipo: 'reja', mensaje: '', privacidad: true }, new Date('2026-10-05T11:00:00Z'));
  assert.equal(r.status, 200);
  assert.equal(avisos.length, 1);
  assert.ok(!JSON.stringify(avisos).includes('Juan') && !JSON.stringify(avisos).includes('669'));
  contact.configure({ store: storeLib.open({ dir, keyHex: KEY }), notify: null }); // "reinicio"
  assert.equal(contact.restore(), 1);
  const rec = storeLib.open({ dir, keyHex: KEY }).all()[0];
  assert.ok(contact.caseIdFor(rec.id));
  contact.configure({ store: null, notify: null });
});

test('formulario: el spam descartado por A3 no se guarda ni genera aviso', () => {
  const contact = require('../src/contact');
  const s = storeLib.open(); const avisos = [];
  contact.configure({ store: s, notify: async (a) => { avisos.push(a); } });
  const r = contact.submit({ nombre: 'Bot', telefono: '600000000', municipio: 'El Paso', tipo: 'otro', mensaje: "' OR 1=1 --", privacidad: true });
  assert.equal(r.status, 200);
  assert.equal(s.all().length, 0); assert.equal(avisos.length, 0);
  contact.configure({ store: null, notify: null });
});

// ---------- comprobación previa a publicar ----------
test('comprobación: con los datos de ejemplo hay bloqueos y se explican en español', () => {
  const { problems } = require('../src/config');
  const { blockers } = problems({});
  const t = blockers.join('\n');
  for (const k of ['NIF', 'domicilio', 'correo', 'alojamiento', 'precios', 'ACOSTA_CLAVE', 'PANEL_CLAVE']) assert.match(t, new RegExp(k, 'i'), k);
});

// ---------- servidor real ----------
function start(env, port) {
  return new Promise((resolve, reject) => {
    const p = spawn(process.execPath, ['server.js'], { cwd: ROOT, env: { ...process.env, PORT: String(port), DATA_DIR: tmp(), ...env } });
    let out = '';
    p.stdout.on('data', (d) => { out += d; if (out.includes('Modo:')) resolve(p); });
    p.stderr.on('data', (d) => { out += d; });
    p.on('exit', (c) => reject(new Error(`salió con ${c}: ${out}`)));
    setTimeout(() => reject(new Error('timeout arrancando')), 8000);
  });
}
const get = (port, p, h = {}) => fetch(`http://127.0.0.1:${port}${p}`, { headers: h, redirect: 'manual' });

test('producción: el servidor se NIEGA a arrancar con datos legales o precios sin validar', () => {
  const r = spawnSync(process.execPath, ['server.js'], { cwd: ROOT, env: { ...process.env, NODE_ENV: 'production', PORT: '3290' }, encoding: 'utf8', timeout: 8000 });
  assert.equal(r.status, 1);
  assert.match(r.stderr, /NO SE PUEDE PUBLICAR/);
  assert.match(r.stderr, /NIF/);
});

test('servidor: web, legales, galería, cabeceras y control de acceso al panel', async () => {
  const p = await start({ PANEL_CLAVE: 'una-clave-larga-123' }, 3291);
  try {
    assert.equal((await get(3291, '/')).status, 200);
    const priv = await (await get(3291, '/privacidad.html')).text();
    assert.match(priv, /Política de privacidad/);
    assert.match(priv, /COMPLETAR/); // en desarrollo se resaltan los datos que faltan
    assert.deepEqual(await (await get(3291, '/api/galeria')).json(), []);
    const h = (await get(3291, '/')).headers;
    assert.match(h.get('content-security-policy'), /default-src 'self'/);
    assert.equal(h.get('x-content-type-options'), 'nosniff');
    assert.equal((await get(3291, '/img/trabajos/.gitkeep')).status, 404);
    assert.equal((await get(3291, '/../server.js')).status, 404);

    const proxy = { 'x-forwarded-for': '8.8.8.8' };
    assert.equal((await get(3291, '/panel', proxy)).status, 401);
    assert.equal((await get(3291, '/api/solicitudes', proxy)).status, 401);
    const mal = { ...proxy, authorization: `Basic ${Buffer.from('jose:otra').toString('base64')}` };
    assert.equal((await get(3291, '/panel', mal)).status, 401);
    const bien = { ...proxy, authorization: `Basic ${Buffer.from('jose:una-clave-larga-123').toString('base64')}` };
    assert.equal((await get(3291, '/panel', bien)).status, 200);
    assert.equal((await get(3291, '/panel')).status, 200); // desde este mismo equipo
  } finally { p.kill(); }
});

test('servidor: sin PANEL_CLAVE el panel es invisible desde fuera', async () => {
  const p = await start({ PANEL_CLAVE: '' }, 3292);
  try {
    assert.equal((await get(3292, '/panel', { 'x-forwarded-for': '8.8.8.8' })).status, 404);
    assert.equal((await get(3292, '/panel')).status, 200);
  } finally { p.kill(); }
});
