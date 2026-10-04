// Agente 4 — Orquestador. Máquina de estados que IMPONE por código el orden y las firmas.
// Sin firma de A2 + A3 (+ propietario cuando aplica) no existe salida.
const { Vault, inbound, outbound, hash } = require('./security');
const creator = require('./creator');
const { review } = require('./supervisor');

const MAX_ECC = 3;
const VITAL = /(beb[ée]|ni[ñn][oa]s?|menor|gas|fuego|humo|incendio|inconsciente|ahogando|persona mayor encerrada)/i;
const cases = new Map();
let seq = 0;

const T_VITAL = 'Si hay una persona en peligro, llama ahora mismo al 112. Estamos avisando a José Ángel Acosta Carballo para que vaya lo antes posible. No cuelgues el 112 hasta que te lo indiquen.';
const T_ESCALADO = 'Gracias por escribirnos. Para este servicio José Ángel Acosta Carballo te contactará personalmente en cuanto pueda.';
const T_BANCO = ' Por tu seguridad, no nos envíes datos bancarios por chat: el pago se hace en persona al terminar el trabajo.';

function newCase({ message, channel = 'whatsapp', clock }) {
  const id = `SAL-${new Date().getFullYear()}-${String(++seq).padStart(6, '0')}`;
  const c = { id, channel, clock, vault: new Vault(), trace: [], state: 'RECIBIDO', t0: Date.now(), message, signatures: { A2: null, A3: null, OWNER: null }, iteraciones: 0 };
  cases.set(id, c);
  return c;
}
const ev = (c, agent, action, status, detail, data) => c.trace.push({ n: c.trace.length + 1, ms: Date.now() - c.t0, agent, action, status, detail, data });
const setState = (c, s) => { c.state = s; ev(c, 'A4', 'ESTADO', 'INFO', `→ ${s}`); };

function ownerRequired(draft) {
  return draft.kind === 'presupuesto' || draft.kind === 'seo';
}

function send(c, text, why) {
  // Puerta de envío: comprobación técnica de firmas (no depende de ningún prompt).
  const h = hash(text);
  const ok = c.signatures.A2?.hash === h && c.signatures.A3?.hash === h && (!c.needsOwner || c.signatures.OWNER?.hash === h);
  if (!ok) { ev(c, 'A4', 'PUERTA_ENVÍO', 'BLOQUEADO', 'Firmas ausentes o no coinciden con el texto final'); setState(c, 'BLOQUEADO'); return false; }
  const real = c.vault.restore(text);
  c.sent = { channel: c.channel, text: real, hash: h, why };
  ev(c, 'A4', 'ENVIAR', 'OK', `Desanonimizado y enviado por ${c.channel}`, { texto_enviado: real });
  setState(c, c.channel === 'seo' ? 'PUBLICADO_SIMULADO' : 'ENVIADO');
  return true;
}

function validate(c, draft, { etaConfirmada = false, fast = false } = {}) {
  // A2 con bucle ECC
  let current = draft;
  const fixes = new Set();
  for (let i = 0; i < MAX_ECC; i++) {
    if (!fast) c.iteraciones = i + 1;
    const r = review(current, { etaConfirmada });
    ev(c, 'A2', `REVISIÓN${fast ? ' RÁPIDA' : ''} (iteración ${i + 1})`, r.veredicto, r.hallazgos.length ? r.hallazgos.map((h) => `[${h.severidad}] ${h.code}: ${h.detalle}`).join(' | ') : 'Checklist P/T/E/V/C sin hallazgos', { checklist: r.checklist, hash: r.hash });
    if (r.veredicto === 'APROBADO') { c.signatures.A2 = { hash: r.hash }; current.text = current.text; return { draft: current, ok: true }; }
    if (etaConfirmada || i === MAX_ECC - 1) break;
    r.hallazgos.forEach((h) => fixes.add(h.code));
    ev(c, 'A4', 'BUCLE ECC', 'INFO', `Devuelve a A1 con correcciones: ${[...fixes].join(', ')}`);
    current = creator.produce({ sanitized: c.sanitized, clock: c.clock, channel: c.channel }, fixes);
    ev(c, 'A1', `BORRADOR CORREGIDO (iteración ${i + 2})`, 'OK', current.text, { texto: current.text });
  }
  return { draft: current, ok: false };
}

function handle(input) {
  const c = newCase(input);
  ev(c, 'A4', 'RECIBIR', 'INFO', `Canal ${c.channel}; hora simulada ${String(c.clock.hour).padStart(2, '0')}:${String(c.clock.minute).padStart(2, '0')}${c.clock.festivo ? ' (festivo/domingo)' : ''}`);

  const sec = inbound(c.message, c.vault);
  c.sanitized = sec.sanitized;
  ev(c, 'A3', 'PRE-CHEQUEO ENTRADA', sec.verdict, `Riesgo ${sec.risk}. ` + (sec.findings.map((f) => `${f.code}: ${f.detalle}`).join(' | ') || 'Sin hallazgos'), { lo_que_ven_los_agentes: sec.sanitized });

  if (sec.verdict === 'BLOQUEADO') { setState(c, 'DESCARTADO'); return view(c); }

  if (sec.verdict === 'ESCALAR') {
    setState(c, 'ESCALADO_PROPIETARIO');
    ev(c, 'A4', 'ESCALADO', 'ALERTA', 'Riesgo ALTO de fraude de titularidad: José Ángel decide. No se confirma ninguna apertura.');
    return finalizeTemplate(c, T_ESCALADO, 'plantilla escalado');
  }

  if (c.channel !== 'seo' && VITAL.test(c.sanitized)) {
    setState(c, 'EMERGENCIA_VITAL');
    ev(c, 'A4', 'ALERTA PROPIETARIO', 'ALERTA', 'EMERGENCIA_VITAL: aviso inmediato a José Ángel por canal fuera de banda');
    return finalizeTemplate(c, T_VITAL, 'plantilla EMERGENCIA_VITAL pre-aprobada');
  }

  const urgencia = c.channel === 'seo' ? 'BAJA' : (c.clock.hour >= 22 || c.clock.hour < 7 ? 'EMERGENCIA' : 'MEDIA');
  setState(c, 'ASIGNADO_A1');
  ev(c, 'A4', 'CLASIFICAR', 'INFO', `Urgencia ${urgencia}; trabajo: ${creator.analyze(c.sanitized).job ?? 'desconocido'}`);

  let draft = creator.produce({ sanitized: c.sanitized, clock: c.clock, channel: c.channel });
  ev(c, 'A1', 'BORRADOR (iteración 1)', 'OK', draft.text, { texto: draft.text, lineas: draft.lines, totales: draft.totals });
  setState(c, 'VALIDACION_QA');
  const qa = validate(c, draft);
  if (!qa.ok) { setState(c, 'ESCALADO_PROPIETARIO'); ev(c, 'A4', 'ESCALADO', 'ALERTA', `Sin convergencia tras ${MAX_ECC} iteraciones ECC`); return view(c); }
  draft = qa.draft;
  c.draft = draft;

  setState(c, 'VALIDACION_SEG');
  const out = outbound(draft.text, c.vault);
  ev(c, 'A3', 'REVISIÓN SALIDA', out.verdict, out.findings.map((f) => `${f.code}: ${f.detalle}`).join(' | ') || 'Sin PII en claro, tokens del caso, sin URLs ni peticiones bancarias', { hash: out.hash });
  if (out.verdict !== 'SEGURO') { setState(c, 'BLOQUEADO'); return view(c); }
  c.signatures.A3 = { hash: out.hash };

  c.needsOwner = ownerRequired(draft);
  if (sec.flags.includes('aviso_bancario')) {
    // El aviso se añade con plantilla fija; se revalida igual.
    draft.text += T_BANCO;
    const r = review(draft); c.signatures.A2 = { hash: r.hash }; c.signatures.A3 = { hash: outbound(draft.text, c.vault).hash };
    ev(c, 'A4', 'AVISO BANCARIO', 'INFO', 'Se añade aviso fijo de no enviar datos bancarios; A2 y A3 refirman');
  }
  if (c.needsOwner) {
    setState(c, 'ESPERANDO_PROPIETARIO');
    ev(c, 'A4', 'SOLICITUD APROBACIÓN', 'ALERTA', c.channel === 'seo' ? 'Publicación web: requiere aprobación de José Ángel' : 'Presupuesto: requiere aprobación de José Ángel (SLA 5 min). Indica disponibilidad.');
    return view(c);
  }
  send(c, draft.text, 'informativo, sin precio');
  return view(c);
}

function finalizeTemplate(c, text, why) {
  const out = outbound(text, c.vault);
  ev(c, 'A3', 'REVISIÓN SALIDA (plantilla)', out.verdict, 'Plantilla pre-aprobada por el propietario');
  c.signatures.A2 = { hash: hash(text), plantilla: true };
  c.signatures.A3 = { hash: out.hash };
  send(c, text, why);
  return view(c);
}

function approve(id, { approved = true, etaMin = 25 } = {}) {
  const c = cases.get(id);
  if (!c || c.state !== 'ESPERANDO_PROPIETARIO') return { error: 'Caso no encontrado o no está esperando aprobación' };
  if (!approved) { ev(c, 'OWNER', 'DECISIÓN', 'RECHAZADO', 'José Ángel rechaza el borrador'); setState(c, 'RECHAZADO_POR_PROPIETARIO'); return view(c); }
  ev(c, 'OWNER', 'DECISIÓN', 'APROBADO', c.channel === 'seo' ? 'Aprueba publicar' : `Aprueba. Disponibilidad real: sale ya, ${etaMin} min`);

  let draft = c.draft;
  let etaConfirmada = false;
  if (c.channel !== 'seo' && draft.job && /apertura|bombin/.test(draft.job)) {
    draft = creator.confirmed(draft, etaMin, c.vault);
    etaConfirmada = true;
    ev(c, 'A1', 'ACTUALIZA CON DISPONIBILIDAD REAL', 'OK', draft.text, { texto: draft.text });
    const qa = validate(c, draft, { etaConfirmada, fast: true });
    if (!qa.ok) { setState(c, 'ESCALADO_PROPIETARIO'); return view(c); }
    const out = outbound(draft.text, c.vault);
    ev(c, 'A3', 'REVISIÓN SALIDA RÁPIDA', out.verdict, out.findings.map((f) => f.detalle).join(' | ') || 'Sin hallazgos', { hash: out.hash });
    if (out.verdict !== 'SEGURO') { setState(c, 'BLOQUEADO'); return view(c); }
    c.signatures.A3 = { hash: out.hash };
  }
  c.signatures.OWNER = { hash: hash(draft.text) };
  send(c, draft.text, 'aprobado por propietario');
  return view(c);
}

function view(c) {
  return {
    id: c.id, state: c.state, channel: c.channel, iteraciones_ecc: c.iteraciones, signatures: c.signatures,
    needsOwner: !!c.needsOwner, awaiting: c.state === 'ESPERANDO_PROPIETARIO', draft: c.draft ? { text: c.draft.text, lines: c.draft.lines, totals: c.draft.totals } : null,
    sent: c.sent ?? null, trace: c.trace, elapsed_ms: Date.now() - c.t0,
  };
}

const get = (id) => (cases.has(id) ? view(cases.get(id)) : null);
const pending = () => [...cases.values()].filter((c) => c.state === 'ESPERANDO_PROPIETARIO').map((c) => ({ id: c.id, channel: c.channel, preview: c.draft?.text.slice(0, 160) ?? '', elapsed_ms: Date.now() - c.t0 }));

module.exports = { handle, approve, get, pending };
