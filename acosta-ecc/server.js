// Servidor local sin dependencias.
//  /              web pública
//  /api/contact   formulario público (solo devuelve mensajes seguros)
//  /panel         consola interna de los agentes (SOLO desde este equipo)
const http = require('http');
const fs = require('fs');
const path = require('path');
const { handle, approve, get, pending } = require('./src/orchestrator');
const contact = require('./src/contact');

const PORT = Number(process.env.PORT) || 3000;
const PUBLIC = path.join(__dirname, 'public');
const MIME = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp',
  '.txt': 'text/plain; charset=utf-8', '.xml': 'application/xml', '.ico': 'image/x-icon',
};
const SITE_CSP = "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; connect-src 'self'; form-action 'self'; base-uri 'self'; frame-ancestors 'none'";
const BASE_HEADERS = { 'X-Content-Type-Options': 'nosniff', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'X-Frame-Options': 'DENY' };

const json = (res, code, body) => { res.writeHead(code, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', ...BASE_HEADERS }); res.end(JSON.stringify(body)); };
const readBody = (req) => new Promise((resolve, reject) => {
  let raw = '';
  req.on('data', (d) => { raw += d; if (raw.length > 20_000) { reject(new Error('Cuerpo demasiado grande')); req.destroy(); } });
  req.on('end', () => { try { resolve(raw ? JSON.parse(raw) : {}); } catch (e) { reject(e); } });
});
// El panel interno solo es accesible desde este mismo equipo y sin proxy intermedio.
const isLocal = (req) => ['127.0.0.1', '::1', '::ffff:127.0.0.1'].includes(req.socket.remoteAddress) && !req.headers['x-forwarded-for'];

const server = http.createServer(async (req, res) => {
  try {
    const url = req.url.split('?')[0];

    if (req.method === 'POST' && url === '/api/contact') {
      if (contact.rateLimited(req.socket.remoteAddress)) return json(res, 429, { error: 'Demasiadas solicitudes. Llámanos al 669 76 86 59.' });
      const r = contact.submit(await readBody(req));
      return json(res, r.status, r.body);
    }

    if (url.startsWith('/api/') || url === '/panel' || url === '/panel.html') {
      if (!isLocal(req)) { res.writeHead(404); return res.end('No encontrado'); }
    }
    if (req.method === 'POST' && url === '/api/case') {
      const b = await readBody(req);
      const [hour, minute] = String(b.time ?? '12:00').split(':').map(Number);
      return json(res, 200, handle({ message: b.message, channel: b.channel === 'seo' ? 'seo' : 'whatsapp', clock: { hour: hour || 0, minute: minute || 0, festivo: !!b.festivo } }));
    }
    if (req.method === 'GET' && url === '/api/pending') return json(res, 200, pending());
    let m = req.method === 'GET' && url.match(/^\/api\/case\/([\w-]+)$/);
    if (m) { const c = get(m[1]); return json(res, c ? 200 : 404, c ?? { error: 'No encontrado' }); }
    m = req.method === 'POST' && url.match(/^\/api\/case\/([\w-]+)\/approve$/);
    if (m) {
      const b = await readBody(req);
      const r = approve(m[1], { approved: b.approved !== false, etaMin: Number(b.etaMin) || 25 });
      return json(res, r.error ? 404 : 200, r);
    }

    const rel = url === '/' ? 'index.html' : url === '/panel' ? 'panel.html' : decodeURIComponent(url).replace(/^\/+/, '');
    const file = path.join(PUBLIC, rel);
    if (!file.startsWith(PUBLIC + path.sep) || !fs.existsSync(file) || !fs.statSync(file).isFile()) { res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' }); return res.end('No encontrado'); }
    const headers = { 'Content-Type': MIME[path.extname(file)] || 'application/octet-stream', ...BASE_HEADERS };
    if (rel !== 'panel.html') headers['Content-Security-Policy'] = SITE_CSP;
    if (/\.(svg|css|js)$/.test(file)) headers['Cache-Control'] = 'no-cache';
    res.writeHead(200, headers);
    fs.createReadStream(file).pipe(res);
  } catch (e) {
    json(res, 400, { error: 'Solicitud no válida' });
  }
});

server.listen(PORT, '127.0.0.1', () => console.log(`Soldadura Acosta · web en http://localhost:${PORT}  ·  panel interno en http://localhost:${PORT}/panel`));
