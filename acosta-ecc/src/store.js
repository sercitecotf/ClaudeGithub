// Almacén de solicitudes cifrado en disco (AES-256-GCM). Sin clave => solo memoria (modo desarrollo).
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

function encrypt(key, obj) {
  const iv = crypto.randomBytes(12);
  const c = crypto.createCipheriv('aes-256-gcm', key, iv);
  const enc = Buffer.concat([c.update(JSON.stringify(obj), 'utf8'), c.final()]);
  return Buffer.concat([iv, c.getAuthTag(), enc]).toString('base64');
}
function decrypt(key, line) {
  const b = Buffer.from(line, 'base64');
  const d = crypto.createDecipheriv('aes-256-gcm', key, b.subarray(0, 12));
  d.setAuthTag(b.subarray(12, 28));
  return JSON.parse(Buffer.concat([d.update(b.subarray(28)), d.final()]).toString('utf8'));
}

function open({ dir, keyHex } = {}) {
  const persistent = !!(dir && keyHex);
  const key = persistent ? Buffer.from(keyHex, 'hex') : null;
  const file = persistent ? path.join(dir, 'solicitudes.enc') : null;
  let rows = [];
  if (persistent) {
    fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
    if (fs.existsSync(file)) rows = fs.readFileSync(file, 'utf8').split('\n').filter(Boolean).map((l) => decrypt(key, l)); // lanza si la clave no es la correcta
  }
  const save = () => {
    if (!persistent) return;
    const tmp = `${file}.tmp`;
    fs.writeFileSync(tmp, rows.map((r) => encrypt(key, r)).join('\n') + (rows.length ? '\n' : ''), { mode: 0o600 });
    fs.renameSync(tmp, file);
  };
  return {
    persistent,
    all: () => rows.map((r) => ({ ...r })),
    get: (id) => { const r = rows.find((x) => x.id === id); return r ? { ...r } : null; },
    append(rec) {
      const r = { id: `W-${Date.now().toString(36)}-${crypto.randomBytes(3).toString('hex')}`, creada: new Date().toISOString(), ...rec };
      rows.push(r); save(); return { ...r };
    },
    update(id, patch) { const r = rows.find((x) => x.id === id); if (!r) return null; Object.assign(r, patch); save(); return { ...r }; },
    purge(months, now = Date.now()) {
      const limit = now - months * 30.44 * 86_400_000;
      const before = rows.length;
      rows = rows.filter((r) => r.estado === 'pendiente' || new Date(r.creada).getTime() >= limit);
      if (rows.length !== before) save();
      return before - rows.length;
    },
  };
}

module.exports = { open };
