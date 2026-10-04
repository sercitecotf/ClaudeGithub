// Agente 2 — Supervisor ECC. Solo lectura: audita y devuelve hallazgos, nunca edita el borrador.
const tarifario = require('../data/tarifario.json');
const catalogo = require('../data/catalogo_servicios.json');
const { totals, eur, norm } = require('./creator');
const { hash } = require('./security');

const TYPOS = [['tecnico', 'técnico'], ['telefono', 'teléfono'], ['direccion', 'dirección'], ['cerrajeria', 'cerrajería'], ['garantia', 'garantía'], ['ningun', 'ningún']];
const INVENTADO = /(más de \d+ años|garant[ií]a de por vida|100\s?%\s?garantizad|los mejores|n[úu]mero\s*1|premiad)/i;
const PROMESA = /(sale ahora|llega(mos)? en \d+|llegada (estimada )?en|en \d+ minutos|ahora mismo)/i;

function review(draft, ctx = {}) {
  const f = [];
  const add = (code, severidad, detalle, fix) => f.push({ code, severidad, detalle, fix });
  const text = draft.text;
  const textNoTokens = text.replace(/\{\{[A-Z]+_\d{3}\}\}/g, '');

  // [P] Precios
  for (const l of draft.lines ?? []) {
    const t = tarifario.tarifas[l.id] ?? Object.values(tarifario.desplazamiento).find((z) => z.id === l.id);
    if (!t) add('P-SIN-TARIFA', 'BLOQUEANTE', `La línea ${l.id} no existe en tarifario.json`, 'Usar solo IDs del tarifario');
    else if (t.importe !== l.importe) add('P-IMPORTE', 'BLOQUEANTE', `${l.id}: ${l.importe} € ≠ tarifario ${t.importe} €`, 'Usar el importe del tarifario');
  }
  if (draft.totals) {
    const calc = totals(draft.lines);
    if (calc.total !== draft.totals.total) add('P-ARITMETICA', 'BLOQUEANTE', `Total ${draft.totals.total} ≠ recalculado ${calc.total}`, 'Recalcular');
    if (!text.includes(eur(calc.total))) add('P-TEXTO-TOTAL', 'MAYOR', 'El texto no muestra el total recalculado', 'Mostrar el total correcto');
  }
  if (draft.kind === 'presupuesto' && (draft.lines ?? []).some((l) => l.tipo === 'desde') && !/desde/.test(text)) {
    add('P-DESDE', 'MAYOR', 'Precio "desde" presentado como cerrado', 'Indicar "desde"');
  }

  // [T] Viabilidad técnica
  const cat = catalogo[draft.job];
  if (cat) {
    if (cat.requiere_visita && draft.totals) add('T-PRECIO-CERRADO', 'BLOQUEANTE', 'Precio cerrado en trabajo que requiere visita', 'Precio orientativo + visita');
    if (cat.requiere_visita && !/visita|valoraci[óo]n/i.test(text)) add('T-FALTA-VISITA', 'MAYOR', 'No indica visita de valoración', 'Añadir visita');
    if (cat.verificar_titularidad && !/acredit/i.test(text)) add('T-TITULARIDAD', 'BLOQUEANTE', 'Apertura sin verificación de titularidad', 'Exigir acreditación al llegar');
    if (cat.ambiente_salino && !/galvaniz|anticorrosi/i.test(text)) add('T-CORROSION', 'MAYOR', 'No menciona protección anticorrosión (ambiente salino de La Palma)', 'Recomendar galvanizado / anticorrosión');
  }
  if (draft.job === 'seo' && !/galvaniz|anticorrosi/i.test(text)) add('T-CORROSION', 'MAYOR', 'Contenido técnico sin protección anticorrosión', 'Añadir mención');

  // [E] Estilo y ortografía
  for (const [mal, bien] of TYPOS) {
    if (new RegExp(`\\b${mal}\\b`, 'i').test(norm(textNoTokens)) && new RegExp(`\\b${mal}\\b`, 'i').test(textNoTokens)) {
      add('E-ORT', 'MENOR', `Ortografía: "${mal}" → "${bien}"`, `Corregir a "${bien}"`);
    }
  }
  if (/\b[A-ZÁÉÍÓÚÑ]{5,}\b/.test(textNoTokens.replace(/IGIC|WHATSAPP/g, ''))) add('E-MAYUSCULAS', 'MENOR', 'Texto en mayúsculas (tono)', 'Usar minúsculas');
  if ((textNoTokens.match(/\p{Extended_Pictographic}/gu) ?? []).length > 1) add('E-EMOJIS', 'MENOR', 'Exceso de emojis para el tono de José Ángel', 'Reducir a uno como máximo');
  if (/jos[eé]\s+[aá]ngel/i.test(text) && !/José Ángel/.test(text)) add('E-NOMBRE', 'MENOR', 'Nombre mal escrito: debe ser "José Ángel"', 'Corregir nombre');

  // [V] Veracidad
  if (INVENTADO.test(text)) add('V-INVENTADO', 'BLOQUEANTE', 'Afirmación no verificable (años, "los mejores", garantías)', 'Eliminar la afirmación');

  // [C] Coherencia / compromisos
  if (PROMESA.test(text) && !ctx.etaConfirmada) add('C-PROMESA', 'MAYOR', 'Promete plazo/salida sin disponibilidad confirmada por el propietario', 'Sustituir por "voy a confirmar disponibilidad"');
  if (draft.kind === 'pregunta' || draft.kind === 'info') { /* informativas: sin comprobaciones de precio */ }

  const uniq = [...new Map(f.map((x) => [x.code, x])).values()];
  const bloquea = uniq.some((x) => x.severidad === 'BLOQUEANTE' || x.severidad === 'MAYOR');
  return {
    veredicto: bloquea ? 'RECHAZADO' : 'APROBADO',
    hallazgos: uniq,
    hash: bloquea ? null : hash(text),
    checklist: { P: !uniq.some((x) => x.code.startsWith('P-')), T: !uniq.some((x) => x.code.startsWith('T-')), E: !uniq.some((x) => x.code.startsWith('E-')), V: !uniq.some((x) => x.code.startsWith('V-')), C: !uniq.some((x) => x.code.startsWith('C-')) },
  };
}

module.exports = { review };
