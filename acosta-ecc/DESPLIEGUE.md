# Cómo publicar la web de Soldadura Acosta

Resumen: un servidor Linux pequeño + Docker. HTTPS (el candado) se activa solo.
Antes de empezar, en tu ordenador: `npm run check` te dice exactamente qué falta.

## 0. Lo que necesitas tener a mano

| Dato | Dónde se rellena |
|---|---|
| NIF, domicilio profesional, correo de contacto | `data/empresa.json` |
| Proveedor de alojamiento (el nombre de la empresa del servidor) | `data/empresa.json` → `proveedor_alojamiento` |
| Plazo de conservación de datos (propuesto: 12 meses) | `data/empresa.json` → `retencion_confirmada: true` |
| Precios reales (y poner `validado_por_propietario: true`) | `data/tarifario.json` |
| Acceso a los DNS de los dos dominios (donde los compraste) | panel del registrador |

**La web se niega a arrancar en producción si falta cualquiera de los datos legales o si los precios siguen siendo de ejemplo.** Es a propósito: así no se publica una web sin aviso legal ni con precios inventados.

## 1. Contratar un servidor

Un VPS Linux (Ubuntu 24.04) de 2 GB de RAM, por ejemplo Hetzner Cloud o DigitalOcean (unos pocos euros al mes).
Apunta la **dirección IP** que te den.

## 2. Apuntar los dominios (DNS)

En el panel donde compraste los dominios, crea registros **A** que apunten a la IP del servidor:

```
soldaduraacosta.es          A   <IP>
www.soldaduraacosta.es      A   <IP>
soldaduraacostabel.com      A   <IP>
www.soldaduraacostabel.com  A   <IP>
```

`soldaduraacosta.es` es el dominio principal; el `.com` y los `www` redirigen a él (se cambia en `Caddyfile`).
Los DNS pueden tardar de minutos a unas horas.

## 3. Preparar el servidor

Conéctate por SSH (en Windows 10: `ssh root@<IP>` desde el CMD) y ejecuta:

```bash
curl -fsSL https://get.docker.com | sh
git clone --branch claude/kind-heisenberg-ebwrxd https://github.com/sercitecotf/ClaudeGithub.git
cd ClaudeGithub/acosta-ecc
```

(El repositorio es privado: GitHub te pedirá usuario y un *token de acceso personal* como contraseña.)

## 4. Rellenar datos y claves

```bash
nano data/empresa.json        # NIF, domicilio, correo, proveedor, retencion_confirmada: true
nano data/tarifario.json      # precios reales y "validado_por_propietario": true
cp .env.example .env
docker run --rm node:22-alpine node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
nano .env                     # pega la clave en ACOSTA_CLAVE y elige PANEL_CLAVE (mín. 12 caracteres)
```

**Guarda `ACOSTA_CLAVE` en un sitio seguro y distinto del servidor** (gestor de contraseñas). Sin ella no se pueden leer las solicitudes guardadas.

Avisos en el móvil (sin datos personales): instala la app **ntfy**, suscríbete a un nombre largo e imposible de adivinar
(p. ej. `acosta-9f3k2x7q-solicitudes`) y ponlo en `NTFY_TOPIC`. Alternativa: un bot de Telegram.

## 5. Arrancar

```bash
docker compose up -d --build
docker compose logs -f app     # debe decir "Modo: PRODUCCIÓN"; si falta algo, lo explica y no arranca
```

Abre https://soldaduraacosta.es. El panel está en https://soldaduraacosta.es/panel (usuario `jose`, contraseña `PANEL_CLAVE`).

## 5b. Prueba antes de dar la web por buena

1. Envía una solicitud desde el formulario. Debe llegar el aviso al móvil y aparecer en el panel.
2. Comprueba `https://soldaduraacosta.es/privacidad.html` y `/aviso-legal.html`: sin ningún «COMPLETAR».
3. Reinicia (`docker compose restart app`): la solicitud debe seguir en el panel.

## Mantenimiento

- **Fotos de trabajos:** copia imágenes `.jpg/.png/.webp` a `public/img/trabajos/`. La galería aparece sola.
  Para pies de foto, crea `public/img/trabajos/leyendas.json`: `{"reja1.jpg": "Reja a medida en Los Llanos"}`. No hace falta reconstruir.
- **Actualizar la web:** `git pull && docker compose up -d --build`
- **Copia de seguridad de las solicitudes** (cifradas): `docker volume ls` para ver el nombre del volumen `..._datos`, y
  `docker run --rm -v <volumen>:/d -v $PWD:/b alpine tar czf /b/copia-datos.tgz -C /d .`
- Las solicitudes antiguas se borran solas pasado el plazo de conservación (las pendientes no).

## Importante

- Esta configuración de Docker/Caddy **no se ha podido probar en contenedor** durante el desarrollo (sin Docker en el entorno de desarrollo);
  sí está probado el servidor en modo producción, el cifrado, los avisos, el panel con contraseña y los bloqueos. Haz la prueba del apartado 5b.
- Los textos legales son una base razonable pero **deben ser revisados por un profesional** (gestor o abogado) antes de publicar.
