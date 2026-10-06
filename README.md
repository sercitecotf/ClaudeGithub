# Asistente de IA para llamadas y citas

Backend gratuito (Node, sin framework) que usa un asistente de voz de Vapi como "herramientas" para consultar, reservar y cancelar citas en Google Calendar.

## 1. Google Calendar (gratis)
1. En Google Cloud Console crea un proyecto y activa **Google Calendar API**.
2. Crea una **cuenta de servicio** y descarga su clave JSON.
3. En Google Calendar, comparte tu calendario con el email de la cuenta de servicio (permiso "Hacer cambios en eventos").
4. Copia el ID del calendario (Configuración del calendario → Integrar calendario).

## 2. Variables de entorno
| Variable | Valor |
|---|---|
| `GOOGLE_CLIENT_EMAIL` | `client_email` del JSON |
| `GOOGLE_PRIVATE_KEY` | `private_key` del JSON |
| `GOOGLE_CALENDAR_ID` | ID del calendario |
| `WEBHOOK_SECRET` | una cadena larga aleatoria |

Edita `config.js` con tu horario y la duración de las citas.

## 3. Despliegue
Sube el repo a Render o Railway (plan gratuito) y usa `npm start`. En Render el plan free se duerme; haz que algún monitor gratuito (UptimeRobot) llame a `GET /` cada 5 minutos.

## 4. Vapi (créditos de prueba)
1. Crea un asistente nuevo con el contenido de `prompt-asistente.md` como prompt de sistema; voz y transcriptor en español.
2. Crea 3 herramientas de tipo *function* con la URL de tu backend y el header `x-vapi-secret`:
   - `consultar_disponibilidad(fecha: "YYYY-MM-DD")`
   - `reservar_cita(fecha, hora "HH:MM", nombre, telefono, servicio)`
   - `cancelar_cita(telefono, fecha)`
3. Asigna un número gratuito de Vapi o prueba con el botón de llamada web.

## Aviso
Informa al inicio de que es una IA y de que se graba, y cumple el RGPD con los datos de tus clientes.
