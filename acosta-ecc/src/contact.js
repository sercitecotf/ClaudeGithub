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

function canaryClock(now = new Date()) {
  const p = Object.fromEntries(new Intl.DateTimeFormat('en-GB', { timeZone: 'Atlantic/Canary', hour: '2-digit', minute: '2-digit', hour12: false, weekday: 'short' }).formatToParts(now).map((x) => [x.type, x.value]));
  return { hour: Number(p.hour) % 24, minute: Number(p.minute), festivo: p.weekday === 'Sun' };
}

const clean = (s, max) => String(s ?? '').replace(/[\u0000-\u001f\u007f]+/g, ' ').replace(/\s+/g, ' ').trim().slice(0, max);

function submit(b, now = new Date()) {
  if (clean(b.website, 50)) return { status: 200, body: { received: true, message: `Gracias, hemos recibido tu solicitud. ${CALL}` } }; // honeypot: no revelamos nada
  const nombre = clean(b.nombre, 60).replace(/[^\p{L}\s'-]/gu, '').trim();
  const telefono = clean(b.telefono, 16);
  const municipio = clean(b.municipio, 40);
  const tipo = clean(b.tipo, 12);
  const mensaje = clean(b.mensaje, 1000);

  if (!nombre || !telefono || !municipio || !(tipo in FRASES)) return { status: 400, body: { error: 'Faltan datos obligatorios.' } };
  if (!TELEFONO.test(telefono)) return { status: 400, body: { error: 'El teléfono no es válido.' } };
  if (!MUNICIPIOS.has(municipio)) return { status: 400, body: { error: 'Municipio no válido.' } };
  if (b.privacidad !== true) return { status: 400, body: { error: 'Debes aceptar la política de privacidad.' } };

  const message = [`Soy ${nombre}.`, FRASES[tipo] && `${FRASES[tipo]} en ${municipio}.`, !FRASES[tipo] && `Estoy en ${municipio}.`, `Mi móvil es ${telefono}.`, mensaje].filter(Boolean).join(' ');
  const r = handle({ message, channel: 'web', clock: canaryClock(now) });

  const first = nombre.split(' ')[0];
  if (r.state === 'ENVIADO' && r.sent) return { status: 200, body: { received: true, message: r.sent.text } }; // plantillas de emergencia / escalado / informativos
  return { status: 200, body: { received: true, message: `Gracias, ${first}. Hemos recibido tu solicitud. José Ángel Acosta Carballo la revisará y te responderá lo antes posible. ${CALL}` } };
}

// Limitador sencillo por IP: 5 solicitudes cada 10 minutos.
const hits = new Map();
function rateLimited(ip, now = Date.now()) {
  const arr = (hits.get(ip) ?? []).filter((t) => now - t < 10 * 60_000);
  arr.push(now);
  hits.set(ip, arr);
  return arr.length > 5;
}

module.exports = { submit, rateLimited, canaryClock };
