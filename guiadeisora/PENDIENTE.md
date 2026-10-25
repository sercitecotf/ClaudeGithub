# Pendiente antes de publicar guiadeisora.net

Los textos son una base. Hay que revisarlos con datos locales reales.

## Obligatorio
- [ ] `aviso-legal.html`: titular, NIF, domicilio y email (LSSI-CE).
- [ ] `privacidad.html`: revisar según analítica/cookies que se usen.
- [ ] Enlaces de afiliado (`href="#"` en excursiones y dormir): darse de alta en GetYourGuide/Civitatis/Booking y sustituir.

## Contenido (buscar los `<!-- TODO -->` en `build.py`)
- [ ] Playas: accesos, aparcamiento, tipo de arena, fotos propias.
- [ ] Excursiones: 2-3 rutas de senderismo con mapa.
- [ ] Dónde comer: 3-5 sitios reales visitados, con reseña propia.
- [ ] Verificar datos (distancias, aeropuerto, guaguas).

## Cómo editar
Cambia el contenido en `build.py` y ejecuta `python3 build.py` para regenerar los HTML.

## Idiomas (es / en / de)
- La web está en español (raíz), inglés (`/en/`) y alemán (`/de/`), con selector de idioma y `hreflang`.
- Las traducciones EN/DE son una primera versión: conviene que las revise un hablante nativo antes de publicar.
- Cada `TODO` de `build.py` existe en los tres idiomas: al rellenar un dato, rellénalo en los tres.
- Más idiomas (nl, fr, it, pl...): se añaden en `../tools/tourism_lib.py` (`LANGS`, `UI`, `COMMON`, `COMERCIOS_UI`) y en `build.py`.

## Comercios de la zona
- Edita `comercios.py` y añade solo negocios reales y verificados (hay un ejemplo en el propio fichero).
- Pide permiso al negocio antes de listarlo. Más adelante se pueden ofrecer posiciones destacadas.
- Regenerar: `python3 build.py`.
