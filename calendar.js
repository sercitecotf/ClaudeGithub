import { google } from "googleapis";
import { config } from "./config.js";

const calendarId = process.env.GOOGLE_CALENDAR_ID;
const auth = new google.auth.JWT({
  email: process.env.GOOGLE_CLIENT_EMAIL,
  key: (process.env.GOOGLE_PRIVATE_KEY || "").replace(/\\n/g, "\n"),
  scopes: ["https://www.googleapis.com/auth/calendar"],
});
const cal = google.calendar({ version: "v3", auth });

// Convierte fecha local (YYYY-MM-DD) + hora (HH:MM) a ISO con la zona del negocio.
function localToDate(fecha, hora) {
  const guess = new Date(`${fecha}T${hora}:00Z`);
  const parts = new Intl.DateTimeFormat("en-US", {
    timeZone: config.timezone, hour12: false,
    year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit",
  }).formatToParts(guess).reduce((a, p) => ((a[p.type] = p.value), a), {});
  const asLocal = Date.UTC(parts.year, parts.month - 1, parts.day, parts.hour % 24, parts.minute);
  return new Date(guess.getTime() - (asLocal - guess.getTime()));
}

export async function huecosLibres(fecha) {
  const dow = new Date(`${fecha}T12:00:00Z`).getUTCDay();
  const franja = config.horario[dow];
  if (!franja) return [];
  const inicio = localToDate(fecha, franja[0]);
  const fin = localToDate(fecha, franja[1]);
  const { data } = await cal.freebusy.query({
    requestBody: { timeMin: inicio.toISOString(), timeMax: fin.toISOString(), items: [{ id: calendarId }] },
  });
  const ocupado = data.calendars[calendarId].busy.map((b) => [new Date(b.start), new Date(b.end)]);
  const paso = config.duracionMinutos * 60000;
  const huecos = [];
  for (let t = inicio.getTime(); t + paso <= fin.getTime(); t += paso) {
    const libre = !ocupado.some(([s, e]) => t < e.getTime() && t + paso > s.getTime());
    if (libre && t > Date.now()) {
      huecos.push(new Intl.DateTimeFormat("es-ES", { timeZone: config.timezone, hour: "2-digit", minute: "2-digit" }).format(t));
    }
  }
  return huecos;
}

export async function reservar({ fecha, hora, nombre, telefono, servicio }) {
  const libres = await huecosLibres(fecha);
  if (!libres.includes(hora)) return { ok: false, motivo: "Ese hueco ya no está disponible" };
  const inicio = localToDate(fecha, hora);
  const fin = new Date(inicio.getTime() + config.duracionMinutos * 60000);
  const { data } = await cal.events.insert({
    calendarId,
    requestBody: {
      summary: `${servicio || "Cita"} - ${nombre}`,
      description: `Teléfono: ${telefono}`,
      start: { dateTime: inicio.toISOString(), timeZone: config.timezone },
      end: { dateTime: fin.toISOString(), timeZone: config.timezone },
      extendedProperties: { private: { telefono } },
    },
  });
  return { ok: true, citaId: data.id };
}

export async function cancelar({ telefono, fecha }) {
  const { data } = await cal.events.list({
    calendarId,
    timeMin: localToDate(fecha, "00:00").toISOString(),
    timeMax: localToDate(fecha, "23:59").toISOString(),
    privateExtendedProperty: `telefono=${telefono}`,
    singleEvents: true,
  });
  if (!data.items?.length) return { ok: false, motivo: "No encuentro ninguna cita con ese teléfono en esa fecha" };
  for (const ev of data.items) await cal.events.delete({ calendarId, eventId: ev.id });
  return { ok: true, canceladas: data.items.length };
}
