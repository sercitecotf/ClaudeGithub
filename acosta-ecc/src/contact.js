// Formulario público -> sistema de agentes.
// El visitante solo recibe un mensaje seguro: nunca la traza, borradores internos ni hallazgos de seguridad.
const tarifario = require('../data/tarifario.json');
const { handle } = require('./orchestrator');

const MUNICIPIOS = new Set(Object.keys(tarifario.desplazamiento));
const FRASES = {
  apertura: 'Necesito una apertura de puerta, me he quedado fuera',
  bombin: 'Necesito cambiar el bombín',
  reja: 'Necesito una reja a medida',
  puerta: 'Necesito un portón metálico a medida',
  soldadura: 'Necesito una soldadura o reparación',
  otro: '',
};
const TELEFONO = /^[+\d][\d\s.-]{8,15}$/;
const CALL = 'Si es urgente, llámanos al 669 76 86 59.';

// Dependencias opcionales (almacén cifrado y avisos). Sin configurar, el módulo funciona igual (modo demo/tests).
let deps = { store: null, notify: null };
const caseByRec = new Map();
const recByCase = new Map();
function configure(d) { deps = { store: d.store ?? null, notify: d.notify ?? null }; }

function canaryClock(now = new Date()) {
  const p = Object.fromEntries(new Intl.DateTimeFormat('en-GB', { timeZone: 'Atlantic/Canary', hour: '2-digit', minute: '2-digit', hour12: false, weekday: 'short' }).formatToParts(now).map((x) => [x.type, x.value]));
  return { hour: Number(p.hour) % 24, minute: Number(p.minute), festivo: p.weekday === 'Sun' };
}

const clean = (s, max) => String(s ?? '').replace(/[\u0000-\u001f\u007f]+/g, ' ').replace(/\s+/g, ' ').trim().slice(0, max);

const buildMessage = ({ nombre, tipo, municipio, telefono, mensaje }) =>
  [`Soy ${nombre}.`, FRASES[tipo] && `${FRASES[tipo]} en ${municipio}.`, !FRASES[tipo] && `Estoy en ${municipio}.`, `Mi móvil es ${telefono}.`, mensaje].filter(Boolean).join(' ');

function link(recId, r) { if (recId) { caseByRec.set(recId, r.id); recByCase.set(r.id, recId); } }

function submit(b, now = new Date()) {
  if (clean(b.website, 50)) return { status: 200, body: { received: true, message: `Gracias, hemos recibido tu solicitud. ${CALL}` } }; // honeypot: no revelamos nada
  const f = {
    nombre: clean(b.nombre, 60).replace(/[^\p{L}\s'-]/gu, '').trim(),
    telefono: clean(b.telefono, 16),
    municipio: clean(b.municipio, 40),
    tipo: clean(b.tipo, 12),
    mensaje: clean(b.mensaje, 1000),
  };
  if (!f.nombre || !f.telefono || !f.municipio || !(f.tipo in FRASES)) return { status: 400, body: { error: 'Faltan datos obligatorios.' } };
  if (!TELEFONO.test(f.telefono)) return { status: 400, body: { error: 'El teléfono no es válido.' } };
  if (!MUNICIPIOS.has(f.municipio)) return { status: 400, body: { error: 'Municipio no válido.' } };
  if (b.privacidad !== true) return { status: 400, body: { error: 'Debes aceptar la política de privacidad.' } };

  const r = handle({ message: buildMessage(f), channel: 'web', clock: canaryClock(now) });
  const first = f.nombre.split(' ')[0];
  const safe = r.state === 'ENVIADO' && r.sent
    ? r.sent.text // plantillas de emergencia / escalado / informativos
    : `Gracias, ${first}. Hemos recibido tu solicitud. José Ángel Acosta Carballo la revisará y te responderá lo antes posible. ${CALL}`;

  // Spam y ataques descartados por A3: no se guardan ni se avisa (no se retienen datos innecesarios).
  if (r.state !== 'DESCARTADO') {
    const urgente = r.trace.some((e) => e.action === 'ALERTA PROPIETARIO' || e.action === 'ESCALADO');
    const pendiente = r.state === 'ESPERANDO_PROPIETARIO' || urgente;
    const rec = deps.store?.append({ ...f, estado: pendiente ? 'pendiente' : 'respondida', urgente });
    link(rec?.id, r);
    Promise.resolve(deps.notify?.({ id: rec?.id ?? r.id, tipo: f.tipo, municipio: f.municipio, urgente })).catch((e) => console.error('[aviso]', e.message));
  }
  return { status: 200, body: { received: true, message: safe } };
}

// Tras un reinicio, las solicitudes pendientes se vuelven a pasar por los agentes para recuperar su borrador.
function restore(now = new Date()) {
  if (!deps.store) return 0;
  const pend = deps.store.all().filter((x) => x.estado === 'pendiente');
  for (const rec of pend) link(rec.id, handle({ message: buildMessage(rec), channel: 'web', clock: canaryClock(now) }));
  return pend.length;
}

const caseIdFor = (recId) => caseByRec.get(recId) ?? null;
function markByCase(caseId) { const id = recByCase.get(caseId); return id ? deps.store?.update(id, { estado: 'atendida' }) : null; }

// Limitador sencillo por IP: `max` intentos cada 10 minutos.
const hits = new Map();
function rateLimited(ip, now = Date.now(), max = 5, bucket = 'c') {
  const k = `${bucket}:${ip}`;
  const arr = (hits.get(k) ?? []).filter((t) => now - t < 10 * 60_000);
  arr.push(now);
  hits.set(k, arr);
  return arr.length > max;
}

module.exports = { submit, rateLimited, canaryClock, configure, restore, caseIdFor, markByCase, buildMessage };
