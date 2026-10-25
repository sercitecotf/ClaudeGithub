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
