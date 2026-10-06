import http from "node:http";
import { huecosLibres, reservar, cancelar } from "./calendar.js";

const tools = {
  consultar_disponibilidad: ({ fecha }) => huecosLibres(fecha),
  reservar_cita: (a) => reservar(a),
  cancelar_cita: (a) => cancelar(a),
};

// Formato de webhook "tool-calls" de Vapi.
async function handle(body) {
  const lista = body?.message?.toolCallList || body?.message?.toolCalls || [];
  const results = [];
  for (const c of lista) {
    const name = c.name || c.function?.name;
    let args = c.arguments || c.function?.arguments || {};
    if (typeof args === "string") args = JSON.parse(args);
    try {
      const r = await tools[name]?.(args);
      results.push({ toolCallId: c.id, result: JSON.stringify(r ?? { error: "herramienta desconocida" }) });
    } catch (e) {
      console.error(e);
      results.push({ toolCallId: c.id, result: JSON.stringify({ error: "Fallo interno" }) });
    }
  }
  return { results };
}

http.createServer(async (req, res) => {
  if (req.method !== "POST" || req.headers["x-vapi-secret"] !== process.env.WEBHOOK_SECRET) {
    res.writeHead(req.method === "GET" ? 200 : 401).end(req.method === "GET" ? "ok" : "no autorizado");
    return;
  }
  let raw = "";
  for await (const ch of req) raw += ch;
  const out = await handle(JSON.parse(raw || "{}"));
  res.writeHead(200, { "content-type": "application/json" }).end(JSON.stringify(out));
}).listen(process.env.PORT || 3000);
