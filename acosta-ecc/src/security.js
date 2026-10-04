// Agente 3 — Seguridad y Privacidad (simulado con reglas deterministas).
// En producción: mismas reglas como herramientas + LLM para casos ambiguos.
const crypto = require('crypto');

const ALLOWED_HOSTS = ['soldaduraacosta.es', 'soldaduraacostabel.com', 'wa.me'];
const hash = (t) => crypto.createHash('sha256').update(t).digest('hex').slice(0, 12);

const RE = {
  iban: /\bES\d{2}(?:[\s-]?\d{4}){5}\b/gi,
  card: /\b(?:\d[ -]?){15,16}\b/g,
  dni: /\b\d{8}[A-Za-z]\b/g,
  email: /[\w.+-]+@[\w-]+\.[\w.-]+/g,
  phone: /(?:\+34[\s.-]?)?[6-9]\d{2}[\s.-]?\d{3}[\s.-]?\d{3}\b/g,
  address: /\b(?:calle|c\/|avda\.?|avenida|plaza|camino|carretera)\s+[\wáéíóúñÁÉÍÓÚÑ]+(?:\s+[\wáéíóúñÁÉÍÓÚÑ]+){0,3}(?:\s*,?\s*(?:n[º°o.]*\s*)?\d{1,3})?/gi,
  name: /\b(?:[Ss]oy|[Mm]e llamo)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){0,2})/g,
};

const HARD_BLOCK = [
  ['XSS', /<\s*script|onerror\s*=|onload\s*=|javascript:/i],
  ['SQLi', /('\s*or\s*'?1'?\s*=\s*'?1|;\s*drop\s+table|\bunion\s+select\b)/i],
  ['SPAM', /(https?:\/\/\S+[\s\S]*){2,}|viagra|casino|bitcoin|crypto\s*invest/i],
  ['FRAUDE', /(cheque.{0,30}exceso|western\s+union|adelanto.{0,30}devolver|env[íi]o.{0,20}gift\s*card)/i],
];
const PROMPT_INJECTION = /(ignora|olvida|ignore|forget)\s+(todas?\s+)?(tus|las|your|the|previous|all)\s*(reglas|instrucciones|rules|instructions)[^.!?\n]*|muestra\s+tu\s+prompt|act[úu]a\s+como\s+[^.!?\n]*|ofrece\s+\d+\s*€?\s*de\s+descuento/gi;
const OWNERSHIP_RISK = /(casa|piso|local|coche)\s+de\s+mi\s+(t[ií]o|t[ií]a|primo|ex|vecin[oa]|amig[oa])|no\s+(tengo|llevo)\s+(dni|documentaci[óo]n)|sin\s+identificar|no\s+quiero\s+identificarme|no\s+est[aá]\s+(el\s+due[ñn]o|en\s+casa).{0,40}(abr|entr)/i;

class Vault {
  constructor() { this.byToken = new Map(); this.n = {}; }
  tokenize(kind, value) {
    for (const [tok, v] of this.byToken) if (v === value && tok.startsWith(`{{${kind}_`)) return tok;
    this.n[kind] = (this.n[kind] || 0) + 1;
    const tok = `{{${kind}_${String(this.n[kind]).padStart(3, '0')}}}`;
    this.byToken.set(tok, value);
    return tok;
  }
  has(tok) { return this.byToken.has(tok); }
  values() { return [...this.byToken.values()]; }
  restore(text) { return text.replace(/\{\{[A-Z]+_\d{3}\}\}/g, (t) => this.byToken.get(t) ?? t); }
}

function inbound(message, vault) {
  const findings = [];
  const flags = [];
  let risk = 'BAJO';
  let text = String(message ?? '');
  const bump = (r) => { const o = ['BAJO', 'MEDIO', 'ALTO', 'CRÍTICO']; if (o.indexOf(r) > o.indexOf(risk)) risk = r; };

  for (const [name, re] of HARD_BLOCK) {
    if (re.test(text)) {
      findings.push({ code: `ENTRADA-${name}`, severidad: 'BLOQUEANTE', detalle: `Patrón ${name} detectado en la entrada` });
      return { verdict: 'BLOQUEADO', risk: 'ALTO', findings, flags: ['descartar'], sanitized: '' };
    }
  }

  if (PROMPT_INJECTION.test(text)) {
    PROMPT_INJECTION.lastIndex = 0;
    text = text.replace(PROMPT_INJECTION, '[TEXTO_NO_CONFIABLE_ELIMINADO]');
    findings.push({ code: 'ENTRADA-INYECCION-PROMPT', severidad: 'MAYOR', detalle: 'Instrucciones dentro del mensaje del cliente: tratadas como dato y eliminadas' });
    bump('MEDIO');
  }

  let bank = false;
  for (const re of [RE.iban, RE.card]) {
    re.lastIndex = 0;
    if (re.test(text)) { re.lastIndex = 0; text = text.replace(re, '[DATO_BANCARIO_ELIMINADO]'); bank = true; }
  }
  if (bank) {
    flags.push('aviso_bancario');
    findings.push({ code: 'RGPD-DATO-BANCARIO', severidad: 'MAYOR', detalle: 'Dato bancario recibido por chat: eliminado, no se almacena ni llega a los agentes' });
    bump('MEDIO');
  }

  const map = [['DNI', RE.dni], ['EMAIL', RE.email], ['TEL', RE.phone], ['DIR', RE.address]];
  for (const [kind, re] of map) {
    re.lastIndex = 0;
    text = text.replace(re, (m) => vault.tokenize(kind, m.trim()));
  }
  RE.name.lastIndex = 0;
  text = text.replace(RE.name, (m, n) => m.replace(n, vault.tokenize('NOM', n)));
  if (vault.byToken.size) findings.push({ code: 'RGPD-TOKENIZACION', severidad: 'INFO', detalle: `${vault.byToken.size} dato(s) personal(es) sustituido(s) por tokens antes de llegar a los agentes de IA` });

  if (OWNERSHIP_RISK.test(text)) {
    findings.push({ code: 'FRAUDE-TITULARIDAD', severidad: 'BLOQUEANTE', detalle: 'Patrón de riesgo: apertura sin titularidad acreditable' });
    return { verdict: 'ESCALAR', risk: 'ALTO', findings, flags: [...flags, 'titularidad_dudosa'], sanitized: text };
  }
  return { verdict: 'SEGURO', risk, findings, flags, sanitized: text };
}

function outbound(text, vault) {
  const findings = [];
  for (const v of vault.values()) {
    if (v && text.includes(v)) findings.push({ code: 'SAL-PII-EN-CLARO', severidad: 'BLOQUEANTE', detalle: 'Dato personal en claro antes de la desanonimización' });
  }
  for (const [name, re] of [['IBAN', RE.iban], ['DNI', RE.dni], ['TELÉFONO', RE.phone], ['EMAIL', RE.email]]) {
    re.lastIndex = 0;
    if (re.test(text)) findings.push({ code: `SAL-${name}`, severidad: 'BLOQUEANTE', detalle: `${name} detectado en el texto de salida` });
  }
  for (const tok of text.match(/\{\{[A-Z]+_\d{3}\}\}/g) ?? []) {
    if (!vault.has(tok)) findings.push({ code: 'SAL-TOKEN-AJENO', severidad: 'BLOQUEANTE', detalle: `Token ${tok} no pertenece a este caso` });
  }
  for (const url of text.match(/https?:\/\/[^\s/]+/gi) ?? []) {
    const host = url.replace(/^https?:\/\//i, '').toLowerCase();
    if (!ALLOWED_HOSTS.some((h) => host === h || host.endsWith(`.${h}`))) findings.push({ code: 'SAL-URL-NO-PERMITIDA', severidad: 'BLOQUEANTE', detalle: `URL fuera de la lista blanca: ${host}` });
  }
  if (/(env[íi]a(me)?|dame|dime|ind[ií]ca(me)?|necesito|facil[ií]ta(me)?|p[aá]sa(me)?).{0,30}(tarjeta|iban|cvv|n[úu]mero de cuenta)/i.test(text)) {
    findings.push({ code: 'SAL-PIDE-DATOS-BANCARIOS', severidad: 'BLOQUEANTE', detalle: 'El texto solicita datos bancarios por chat' });
  }
  const blocked = findings.some((f) => f.severidad === 'BLOQUEANTE');
  return { verdict: blocked ? 'BLOQUEADO' : 'SEGURO', risk: blocked ? 'ALTO' : 'BAJO', findings, hash: hash(text) };
}

module.exports = { Vault, inbound, outbound, hash };
