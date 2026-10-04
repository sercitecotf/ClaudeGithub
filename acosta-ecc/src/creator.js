// Agente 1 — Creación y Atención (SIMULADO con plantillas).
// En producción este módulo es una llamada a un LLM con el system prompt de la documentación.
// Para que la demo enseñe el bucle ECC, el primer borrador incluye fallos típicos
// (promesa de plazo, tilde, afirmación inventada, falta de aviso anticorrosión) que el
// Supervisor detecta; el creador los corrige cuando recibe `fixes`.
const tarifario = require('../data/tarifario.json');
const catalogo = require('../data/catalogo_servicios.json');

const norm = (s) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
const eur = (n) => `${n.toFixed(2).replace('.', ',')} €`;
const round2 = (n) => Math.round(n * 100) / 100;

function detectMunicipio(text) {
  const t = norm(text);
  for (const [name, z] of Object.entries(tarifario.desplazamiento)) {
    if ([norm(name), ...z.alias].some((a) => t.includes(a))) return name;
  }
  return null;
}

function detectJob(text) {
  const t = norm(text);
  if (/(quedado fuera|llaves dentro|abrir (la )?puerta|apertura|cerradura bloquead|no puedo entrar)/.test(t)) return 'apertura';
  if (/(bombin|cilindro)/.test(t)) return 'bombin';
  if (/reja/.test(t)) return 'reja';
  if (/(porton|puerta metalica|puerta de hierro)/.test(t)) return 'puerta_metalica';
  if (/(solda|reparar|reparacion)/.test(t)) return 'soldadura';
  return null;
}

function analyze(text) {
  return { job: detectJob(text), municipio: detectMunicipio(text) };
}

function computeLines(job, municipio, clock) {
  const lines = [];
  const add = (id, qty = 1) => {
    const t = tarifario.tarifas[id];
    lines.push({ id, concepto: t.concepto, importe: t.importe, qty, tipo: t.tipo || 'cerrado', unidad: t.unidad });
  };
  add(catalogo[job].tarifa);
  if (!catalogo[job].requiere_visita) {
    const h = clock.hour;
    if (h >= 22 || h < 7) add('REC-NOC-01');
    if (clock.festivo) add('REC-FES-01');
    const z = tarifario.desplazamiento[municipio];
    lines.push({ id: z.id, concepto: `Desplazamiento a ${municipio}`, importe: z.importe, qty: 1, tipo: 'cerrado' });
  }
  return lines;
}

function totals(lines) {
  const subtotal = round2(lines.reduce((s, l) => s + l.importe * l.qty, 0));
  const igic = round2(subtotal * tarifario.igic);
  return { subtotal, igic, total: round2(subtotal + igic) };
}

function produce(ctx, fixes = new Set()) {
  const { sanitized, clock, channel } = ctx;
  const { job, municipio } = analyze(sanitized);
  const hola = /\{\{NOM_\d{3}\}\}/.test(sanitized) ? `Hola ${sanitized.match(/\{\{NOM_\d{3}\}\}/)[0]}` : 'Hola';
  const dir = /\{\{DIR_\d{3}\}\}/.exec(sanitized)?.[0];

  if (channel === 'seo') return produceSeo(sanitized, municipio, fixes);

  if (!job) {
    return { kind: 'info', job: null, lines: [], totals: null, meta: { municipio },
      text: `${hola}, gracias por escribirnos. Para ayudarte mejor, ¿puedes contarme qué trabajo necesitas (cerrajería, reja, puerta o soldadura) y en qué zona de La Palma estás? Si es algo fuera de lo habitual, se lo consulto a José Ángel Acosta Carballo.` };
  }
  if (!municipio) {
    return { kind: 'pregunta', job, lines: [], totals: null, meta: {},
      text: `${hola}, gracias por escribirnos. ¿En qué municipio de La Palma estás? Así calculo el desplazamiento y te preparo el presupuesto.` };
  }

  const lines = computeLines(job, municipio, clock);
  const t = catalogo[job].requiere_visita ? null : totals(lines);
  const flawed = (code) => !fixes.has(code);
  let text;

  if (job === 'apertura' || job === 'bombin') {
    const partes = lines.map((l) => { const c = l.concepto.split(' (')[0]; return `${c[0].toLowerCase()}${c.slice(1)} ${eur(l.importe)}`; }).join(' + ');
    text =
      `${hola}, gracias por escribirnos. Para ${job === 'apertura' ? 'la apertura sin daños' : 'el cambio de bombín'} en ` +
      `${flawed('E-ORT') ? 'la direccion' : 'la dirección'} ${dir ?? 'indicada'} (${municipio}) el presupuesto es: ${partes}` +
      ` = ${eur(t.subtotal)} + IGIC (7 %) ${eur(t.igic)} = ${eur(t.total)}. ` +
      'Si la cerradura fuera de alta seguridad podría requerir otro método y te avisaríamos antes. ' +
      'Al llegar, el técnico te pedirá que acredites que vives en la vivienda (DNI o recibo a tu nombre). ' +
      'El pago se hace en el momento, al terminar el trabajo. ' +
      (flawed('C-PROMESA')
        ? 'El técnico sale ahora mismo y llega en 15 minutos.'
        : 'Voy a confirmar la disponibilidad del técnico y te aviso en unos minutos.');
  } else {
    const l = lines[0];
    text =
      `${hola}, gracias por escribirnos. Para ${catalogo[job].nombre.toLowerCase()} en ${municipio}: trabajamos a medida y el precio orientativo es desde ${eur(l.importe)}/${l.unidad} (IGIC no incluido). ` +
      (flawed('T-CORROSION') ? '' : 'Por el ambiente salino de la isla recomendamos acabado galvanizado o pintura anticorrosión. ') +
      'El precio final se confirma tras una visita de valoración con las medidas exactas. ¿Nos envías unas fotos y las medidas aproximadas?';
  }
  return { kind: 'presupuesto', job, lines, totals: t, meta: { municipio }, text };
}

function produceSeo(topic, municipio, fixes) {
  const zona = municipio ?? 'La Palma';
  const experiencia = fixes.has('V-INVENTADO') ? '' : ' Con más de 30 años de experiencia, somos los mejores de la isla.';
  return {
    kind: 'seo', job: 'seo', lines: [], totals: null, meta: { municipio },
    text:
      `# Rejas a medida en ${zona} | Soldadura Acosta\n\n` +
      `En Soldadura Acosta La Palma, dirigida por José Ángel Acosta Carballo, fabricamos rejas de hierro a medida para ventanas y puertas en ${zona}.${experiencia}\n\n` +
      'Por el ambiente salino de la isla, trabajamos con acabado galvanizado o pintura anticorrosión para que la reja dure más.\n\n' +
      'Pide tu presupuesto sin compromiso en soldaduraacosta.es: visitamos, medimos y te confirmamos el precio final.',
  };
}

// Tras la confirmación del propietario, el creador incorpora la disponibilidad real.
function confirmed(draft, etaMin, vault) {
  const dir = [...vault.byToken.keys()].find((k) => k.startsWith('{{DIR_'));
  const text = draft.text.replace(
    'Voy a confirmar la disponibilidad del técnico y te aviso en unos minutos.',
    `Confirmado: José Ángel sale ya${dir ? ` hacia ${dir}` : ''}, llegada estimada en unos ${etaMin} minutos.`,
  );
  return { ...draft, text };
}

module.exports = { produce, confirmed, analyze, totals, eur, norm };
