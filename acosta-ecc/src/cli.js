// Demo por terminal: caso de cerrajería a medianoche en Los Llanos de Aridane.
const { handle, approve } = require('./orchestrator');

const COLORS = { A1: '\x1b[36m', A2: '\x1b[33m', A3: '\x1b[35m', A4: '\x1b[32m', OWNER: '\x1b[34m' };
const print = (trace, from = 0) => trace.slice(from).forEach((e) => {
  const d = e.detail.length > 220 ? `${e.detail.slice(0, 220)}…` : e.detail;
  console.log(`${COLORS[e.agent] ?? ''}${String(e.ms).padStart(4)}ms [${e.agent}] ${e.action} · ${e.status}\x1b[0m ${d}`);
});

const r = handle({
  message: 'Hola, soy María, me he quedado fuera de casa con las llaves dentro, estoy en calle Cruz Roja 14, Los Llanos. Mi móvil es 612 345 678. Necesito alguien YA por favor',
  channel: 'whatsapp',
  clock: { hour: 0, minute: 12, festivo: true },
});
print(r.trace);
console.log('\n— José Ángel aprueba: sale ya, 25 min —\n');
const n = r.trace.length;
const f = approve(r.id, { approved: true, etaMin: 25 });
print(f.trace, n);
console.log(`\nEstado final: ${f.state} · iteraciones ECC: ${f.iteraciones_ecc}\n\nMENSAJE ENVIADO AL CLIENTE:\n${f.sent?.text}`);
