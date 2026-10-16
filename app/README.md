# Qualitus Next

Reemplazo del sistema APPCC/HACCP actual (ver `analysis/qualitus-webapp/` en
la raíz del repo para el análisis que originó este proyecto). Construido
desde cero, priorizando no romper nada y no necesitar mantenimiento
constante: stack aburrido y probado (Django), seguridad por defecto, y
pruebas automáticas desde el primer módulo.

## Por qué Django

Se eligió explícitamente por ser "seguro y que no dé problemas":
defaults de seguridad fuertes (CSRF, protección XSS, cabeceras, validación
de contraseñas), ORM maduro con migraciones versionadas, panel de
administración incluido para las pantallas internas que no necesitan UI a
medida, y un ciclo de vida de soporte muy largo (Qualitus actual lleva
años sin soporte del proveedor original — esto es justo lo que se quiere
evitar que vuelva a pasar).

## Estado

**Primer módulo construido: Puntos de Control.** Es el núcleo del sistema
APPCC — de él dependen (o se espera que dependan más adelante) Temperatura,
Agua, Limpieza, Inspecciones y Análisis. Ver
`analysis/qualitus-webapp/README.md` para por qué se eligió este módulo
primero.

Incluye:
- Modelo `ControlPoint` con las mismas columnas vistas en la captura de
  Qualitus (objeto, categoría, nombre, tipo de dato, valores aceptables,
  unidad de medida, requisito, crítico), con validación a nivel de modelo
  (no solo de formulario): un punto numérico siempre necesita rango y
  unidad; uno de checkbox/texto no puede llevar rango numérico.
- Lista con buscador y paginación (equivalente a "Mostrando 1-20 de N en
  total" de Qualitus) y detalle, ambos protegidos por login.
- Panel de administración (`/admin/`) para altas/bajas mientras no haya
  formularios propios.
- 12 pruebas automáticas (modelo + vistas) — corren en cada cambio, no son
  documentación que se desactualiza.

**Sin construir todavía:** el resto de los 21 módulos del menú, y la
integración con SAP Business One (Service Layer) para Proveedores y
Materias Primas/Productos — queda pendiente de que el usuario dé acceso a
la conexión ya existente (ver `analysis/qualitus-webapp/README.md`,
sección "Requisito para la reconstrucción").

## Cómo correrlo en local

```bash
cd app
pip install -r requirements.txt
cp .env.example .env
python3 -c "from django.core.management.utils import get_random_secret_key as k; print(k())"
# pega el resultado como DJANGO_SECRET_KEY en .env, y deja DJANGO_DEBUG=True

python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```

Luego entra a `http://127.0.0.1:8000/` (pide login) y a
`http://127.0.0.1:8000/admin/` para cargar puntos de control de prueba.

## Cómo correr las pruebas

```bash
python3 manage.py test
```

## Decisiones de seguridad ya tomadas

- Nada de secretos en el código: todo sale de variables de entorno
  (`.env`, que está en `.gitignore`; `.env.example` documenta qué hace
  falta).
- `DEBUG=False` por defecto; hay que activarlo explícitamente en local.
- Con `DEBUG=False` se activan automáticamente HSTS, cookies de sesión y
  CSRF solo-HTTPS, `X-Frame-Options: DENY` y `nosniff` — no dependen de que
  alguien se acuerde de configurarlos aparte en producción.
- Sesión de 8 horas por inactividad.
- Modelo de usuario propio (`accounts.User`) desde el día uno, para no
  quedar atado al de Django si luego hace falta vincular usuarios con SAP
  o con el árbol de permisos que tenía Qualitus.
- Validación de integridad en el modelo (`ControlPoint.clean()`), no solo
  en el formulario: los datos quedan correctos aunque se carguen por script,
  fixture o el admin.
