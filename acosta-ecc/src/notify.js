// Avisos a José Ángel. IMPORTANTE: los avisos NUNCA llevan datos personales del cliente
// (ni nombre, ni teléfono, ni dirección): solo el tipo de trabajo, el municipio y el número de caso.
const TIPOS = { apertura: 'apertura de puerta', bombin: 'cambio de bombín', reja: 'reja a medida', puerta: 'puerta o portón metálico', soldadura: 'soldadura o reparación', otro: 'otra consulta' };

async function post(url, init) {
  const res = await fetch(url, { ...init, signal: AbortSignal.timeout(5000) });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
}

async function notify({ id, tipo, municipio, urgente }, env = process.env) {
  const panel = env.PANEL_URL ? ` Ábrela en ${env.PANEL_URL}` : ' Ábrela en el panel.';
  const texto = `${urgente ? 'URGENTE: ' : ''}Nueva solicitud web ${id}: ${TIPOS[tipo] ?? 'consulta'} en ${municipio}.${panel}`;
  const jobs = [];
  if (env.NTFY_TOPIC) jobs.push(post(`https://ntfy.sh/${encodeURIComponent(env.NTFY_TOPIC)}`, { method: 'POST', body: texto, headers: { Title: 'Soldadura Acosta', Priority: urgente ? 'urgent' : 'default' } }));
  if (env.TELEGRAM_BOT_TOKEN && env.TELEGRAM_CHAT_ID) jobs.push(post(`https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendMessage`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ chat_id: env.TELEGRAM_CHAT_ID, text: texto }) }));
  const res = await Promise.allSettled(jobs);
  res.filter((r) => r.status === 'rejected').forEach((r) => console.error('[aviso] fallo al notificar:', r.reason?.message));
  return { sent: res.filter((r) => r.status === 'fulfilled').length, texto };
}

module.exports = { notify };
