// Servidor local sin dependencias: sirve la UI y expone la API del orquestador.
const http = require('http');
const fs = require('fs');
const path = require('path');
const { handle, approve } = require('./src/orchestrator');

const PORT = Number(process.env.PORT) || 3000;
const PUBLIC = path.join(__dirname, 'public');
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json' };

const json = (res, code, body) => { res.writeHead(code, { 'Content-Type': 'application/json; charset=utf-8' }); res.end(JSON.stringify(body)); };
const readBody = (req) => new Promise((resolve, reject) => {
  let raw = '';
  req.on('data', (d) => { raw += d; if (raw.length > 20_000) { reject(new Error('Cuerpo demasiado grande')); req.destroy(); } });
  req.on('end', () => { try { resolve(raw ? JSON.parse(raw) : {}); } catch (e) { reject(e); } });
});

const server = http.createServer(async (req, res) => {
  try {
    if (req.method === 'POST' && req.url === '/api/case') {
      const b = await readBody(req);
      const [hour, minute] = String(b.time ?? '12:00').split(':').map(Number);
      return json(res, 200, handle({ message: b.message, channel: b.channel === 'seo' ? 'seo' : 'whatsapp', clock: { hour: hour || 0, minute: minute || 0, festivo: !!b.festivo } }));
    }
    const m = req.method === 'POST' && req.url.match(/^\/api\/case\/([\w-]+)\/approve$/);
    if (m) {
      const b = await readBody(req);
      const r = approve(m[1], { approved: b.approved !== false, etaMin: Number(b.etaMin) || 25 });
      return json(res, r.error ? 404 : 200, r);
    }
    const file = path.join(PUBLIC, req.url === '/' ? 'index.html' : req.url.split('?')[0]);
    if (!file.startsWith(PUBLIC) || !fs.existsSync(file)) { res.writeHead(404); return res.end('No encontrado'); }
    res.writeHead(200, { 'Content-Type': MIME[path.extname(file)] || 'application/octet-stream' });
    fs.createReadStream(file).pipe(res);
  } catch (e) {
    json(res, 400, { error: e.message });
  }
});

server.listen(PORT, '127.0.0.1', () => console.log(`Soldadura Acosta · demo ECC en http://localhost:${PORT}`));
