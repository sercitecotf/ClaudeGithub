// Configuración y comprobaciones previas a publicar.
const fs = require('fs');
const path = require('path');
const fsPath = (f) => path.join(__dirname, '..', 'data', f);
const read = (f) => JSON.parse(fs.readFileSync(fsPath(f), 'utf8'));

const empresa = () => read('empresa.json');
const isProduction = (env = process.env) => env.NODE_ENV === 'production';
const galleryDir = path.join(__dirname, '..', 'public', 'img', 'trabajos');
const galleryFiles = () => (fs.existsSync(galleryDir) ? fs.readdirSync(galleryDir).filter((f) => /\.(jpe?g|png|webp)$/i.test(f)).sort() : []);

function problems(env = process.env) {
  const emp = empresa();
  const tar = read('tarifario.json');
  const blockers = [];
  const warnings = [];
  const need = [['nif', 'NIF'], ['domicilio', 'domicilio profesional'], ['email', 'correo electrónico de contacto'], ['proveedor_alojamiento', 'proveedor de alojamiento (ej. Hetzner)']];
  for (const [k, label] of need) if (!emp[k] || !String(emp[k]).trim()) blockers.push(`Falta en data/empresa.json: ${label} (campo «${k}»).`);
  if (emp.retencion_confirmada !== true) blockers.push('Confirma el plazo de conservación de datos (data/empresa.json: «retencion_meses» y «retencion_confirmada»: true).');
  if (tar.validado_por_propietario !== true) blockers.push('Los precios de data/tarifario.json son de ejemplo: pon los reales y «validado_por_propietario»: true.');
  if (!/^[0-9a-f]{64}$/i.test(env.ACOSTA_CLAVE || '')) blockers.push('Falta ACOSTA_CLAVE (clave de cifrado de 64 caracteres hex). Genérala con: npm run generar-clave');
  if ((env.PANEL_CLAVE || '').length < 12) blockers.push('Falta PANEL_CLAVE (contraseña del panel, mínimo 12 caracteres).');
  if (!env.NTFY_TOPIC && !(env.TELEGRAM_BOT_TOKEN && env.TELEGRAM_CHAT_ID)) warnings.push('Sin avisos: configura NTFY_TOPIC o TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID para enterarte de cada solicitud.');
  if (!galleryFiles().length) warnings.push('La galería está vacía: añade fotos de trabajos reales en public/img/trabajos/.');
  return { blockers, warnings };
}

module.exports = { empresa, isProduction, problems, galleryFiles, galleryDir };
