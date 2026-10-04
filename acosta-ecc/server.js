// Servidor sin dependencias.
//  /               web pública            /api/contact   formulario público (solo mensajes seguros)
//  /panel          panel interno (solo desde este equipo, o con contraseña PANEL_CLAVE)
const http = require('http');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { handle, approve, get } = require('./src/orchestrator');
const contact = require('./src/contact');
const config = require('./src/config');
const legal = require('./src/legal');
const storeLib = require('./src/store');
const { notify } = require('./src/notify');

const PORT = Number(process.env.PORT) || 3000;
const HOST = process.env.HOST || '127.0.0.1';
const PUBLIC = path.join(__dirname, 'public');
const DATA_DIR = process.env.DATA_DIR || path.join(__dirname, 'datos');
const PROD = config.isProduction();

const MIME = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp',
  '.txt': 'text/plain; charset=utf-8', '.xml': 'application/xml', '.ico': 'image/x-icon',
};
const SITE_CSP = "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; connect-src 'self'; form-action 'self'; base-uri 'self'; frame-ancestors 'none'";
const BASE_HEADERS = { 'X-Content-Type-Options': 'nosniff', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'X-Frame-Options': 'DENY' };

// ---------- arranque seguro ----------
if (PROD) {
  const { blockers } = config.problems();
  if (blockers.length) {
    console.error('\nNO SE PUEDE PUBLICAR todavía. Falta lo siguiente:\n');
    blockers.forEach((b) => console.error(`  ✖ ${b}`));
    console.error('\nComprueba el estado con: npm run check\n');
    process.exit(1);
  }
}
let store;
try { store = storeLib.open({ dir: DATA_DIR, keyHex: process.env.ACOSTA_CLAVE }); } catch (e) {
  console.error('\nNo se pueden leer las solicitudes guardadas: ACOSTA_CLAVE no coincide con la usada al guardarlas, o el archivo está dañado.\nNo se arranca para no perder ni sobrescribir datos.\n');
  process.exit(1);
}
store.purge(config.empresa().retencion_meses ?? 12);
contact.configure({ store, notify });
const restored = contact.restore();

// ---------- utilidades ----------
const json = (res, code, body, extra = {}) => { res.writeHead(code, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', ...BASE_HEADERS, ...extra }); res.end(JSON.stringify(body)); };
const readBody = (req) => new Promise((resolve, reject) => {
  let raw = '';
  req.on('data', (d) => { raw += d; if (raw.length > 20_000) { reject(new Error('Cuerpo demasiado grande')); req.destroy(); } });
  req.on('end', () => { try { resolve(raw ? JSON.parse(raw) : {}); } catch (e) { reject(e); } });
});
const clientIp = (req) => (process.env.TRUST_PROXY === '1' ? String(req.headers['x-forwarded-for'] ?? '').split(',')[0].trim() : '') || req.socket.remoteAddress;
const isLocal = (req) => ['127.0.0.1', '::1', '::ffff:127.0.0.1'].includes(req.socket.remoteAddress) && !req.headers['x-forwarded-for'];
const sha = (s) => crypto.createHash('sha256').update(String(s)).digest();

// Acceso al panel: desde este equipo, o con usuario "jose" y la contraseña PANEL_CLAVE (con HTTPS).
function panelAccess(req) {
  if (isLocal(req)) return 'ok';
  const pass = process.env.PANEL_CLAVE;
  if (!pass) return 'hidden';
  if (contact.rateLimited(clientIp(req), Date.now(), 20, 'auth')) return 'blocked';
  const m = /^Basic (.+)$/.exec(req.headers.authorization ?? '');
  if (m) {
    const [u, ...rest] = Buffer.from(m[1], 'base64').toString('utf8').split(':');
    if (u === 'jose' && crypto.timingSafeEqual(sha(rest.join(':')), sha(pass))) return 'ok';
  }
  return 'login';
}

const publicRec = (r) => ({ id: r.id, creada: r.creada, estado: r.estado, tipo: r.tipo, municipio: r.municipio, urgente: !!r.urgente });

const server = http.createServer(async (req, res) => {
  try {
    const url = req.url.split('?')[0];

    if (req.method === 'POST' && url === '/api/contact') {
      if (contact.rateLimited(clientIp(req))) return json(res, 429, { error: 'Demasiadas solicitudes. Llámanos al 669 76 86 59.' });
      const r = contact.submit(await readBody(req));
      return json(res, r.status, r.body);
    }

    if (req.method === 'GET' && url === '/api/galeria') {
      const caps = fs.existsSync(path.join(config.galleryDir, 'leyendas.json')) ? JSON.parse(fs.readFileSync(path.join(config.galleryDir, 'leyendas.json'), 'utf8')) : {};
      return json(res, 200, config.galleryFiles().slice(0, 24).map((f) => ({ src: `img/trabajos/${f}`, alt: caps[f] || 'Trabajo realizado por Soldadura Acosta' })), { 'Cache-Control': 'public, max-age=60' });
    }

    if (req.method === 'GET' && (url === '/privacidad.html' || url === '/aviso-legal.html')) {
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', ...BASE_HEADERS, 'Content-Security-Policy': SITE_CSP });
      return res.end((url === '/privacidad.html' ? legal.privacidad : legal.avisoLegal)(config.empresa()));
    }

    // ----- zona interna -----
    if (url.startsWith('/api/') || url === '/panel' || url === '/panel.html') {
      const access = panelAccess(req);
      if (access === 'hidden') { res.writeHead(404); return res.end('No encontrado'); }
      if (access === 'blocked') return json(res, 429, { error: 'Demasiados intentos' });
      if (access === 'login') { res.writeHead(401, { 'WWW-Authenticate': 'Basic realm="Panel Soldadura Acosta", charset="UTF-8"', ...BASE_HEADERS }); return res.end('Acceso restringido'); }
    }
    if (req.method === 'POST' && url === '/api/case') {
      const b = await readBody(req);
      const [hour, minute] = String(b.time ?? '12:00').split(':').map(Number);
      return json(res, 200, handle({ message: b.message, channel: b.channel === 'seo' ? 'seo' : 'whatsapp', clock: { hour: hour || 0, minute: minute || 0, festivo: !!b.festivo } }));
    }
    if (req.method === 'GET' && url === '/api/solicitudes') return json(res, 200, store.all().reverse().map((r) => ({ ...publicRec(r), caseId: contact.caseIdFor(r.id) })));
    let m = req.method === 'GET' && url.match(/^\/api\/solicitud\/([\w-]+)$/);
    if (m) {
      const r = store.get(m[1]);
      if (!r) return json(res, 404, { error: 'No encontrada' });
      const caseId = contact.caseIdFor(r.id);
      return json(res, 200, { ...r, caso: caseId ? get(caseId) : null });
    }
    m = req.method === 'POST' && url.match(/^\/api\/solicitud\/([\w-]+)\/atendida$/);
    if (m) { const r = store.update(m[1], { estado: 'atendida' }); return json(res, r ? 200 : 404, r ? publicRec(r) : { error: 'No encontrada' }); }
    m = req.method === 'GET' && url.match(/^\/api\/case\/([\w-]+)$/);
    if (m) { const c = get(m[1]); return json(res, c ? 200 : 404, c ?? { error: 'No encontrado' }); }
    m = req.method === 'POST' && url.match(/^\/api\/case\/([\w-]+)\/approve$/);
    if (m) {
      const b = await readBody(req);
      const r = approve(m[1], { approved: b.approved !== false, etaMin: Number(b.etaMin) || 25 });
      if (!r.error && b.approved !== false) contact.markByCase(m[1]);
      return json(res, r.error ? 404 : 200, r);
    }

    // ----- archivos estáticos -----
    const rel = url === '/' ? 'index.html' : url === '/panel' ? 'panel.html' : decodeURIComponent(url).replace(/^\/+/, '');
    const file = path.join(PUBLIC, rel);
    if (!file.startsWith(PUBLIC + path.sep) || !fs.existsSync(file) || !fs.statSync(file).isFile() || path.basename(file).startsWith('.')) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' }); return res.end('No encontrado');
    }
    const headers = { 'Content-Type': MIME[path.extname(file)] || 'application/octet-stream', ...BASE_HEADERS };
    if (rel !== 'panel.html') headers['Content-Security-Policy'] = SITE_CSP;
    headers['Cache-Control'] = /\.(svg|css|js|html)$/.test(file) ? 'no-cache' : 'public, max-age=3600';
    res.writeHead(200, headers);
    fs.createReadStream(file).pipe(res);
  } catch (e) {
    json(res, 400, { error: 'Solicitud no válida' });
  }
});

server.listen(PORT, HOST, () => {
  console.log(`Soldadura Acosta · web en http://localhost:${PORT}  ·  panel interno en http://localhost:${PORT}/panel`);
  console.log(`Modo: ${PROD ? 'PRODUCCIÓN' : 'desarrollo'} · almacén ${store.persistent ? `cifrado en ${DATA_DIR}` : 'solo en memoria (sin ACOSTA_CLAVE)'}${restored ? ` · ${restored} solicitud(es) pendiente(s) recuperada(s)` : ''}`);
});
