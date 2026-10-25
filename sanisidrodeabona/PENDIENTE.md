# Pendiente antes de publicar sanisidrodeabona.com

## Obligatorio
- [ ] `aviso-legal.html` / `privacidad.html`: datos reales del titular.
- [ ] Enlaces de afiliado (`href="#"`): alta en Booking y GetYourGuide/Civitatis.
- [ ] **Correo:** este dominio se usa para email. Al configurar el DNS de la web, NO borres los registros MX/SPF/DKIM del correo.

## Contenido (buscar `<!-- TODO -->` en `build.py`)
- [ ] Lugares concretos del pueblo con fotos propias.
- [ ] Fechas de las fiestas (consultar ayuntamiento).
- [ ] Tiempos de trayecto al aeropuerto y alojamientos reales.
- [ ] 3-5 sitios para comer visitados.

## Idiomas (es / en / de)
- La web está en español (raíz), inglés (`/en/`) y alemán (`/de/`), con selector de idioma y `hreflang`.
- Las traducciones EN/DE son una primera versión: conviene que las revise un hablante nativo antes de publicar.
- Cada `TODO` de `build.py` existe en los tres idiomas: al rellenar un dato, rellénalo en los tres.
- Más idiomas (nl, fr, it, pl...): se añaden en `../tools/tourism_lib.py` (`LANGS`, `UI`, `COMMON`, `COMERCIOS_UI`) y en `build.py`.

## Comercios de la zona
- Edita `comercios.py` y añade solo negocios reales y verificados (hay un ejemplo en el propio fichero).
- Pide permiso al negocio antes de listarlo. Más adelante se pueden ofrecer posiciones destacadas.
- Regenerar: `python3 build.py`.
