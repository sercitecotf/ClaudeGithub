"""
Django settings for qualitus_next project.

Decisiones de seguridad tomadas a propósito (ver analysis/qualitus-webapp/
README.md para el contexto del proyecto que reemplaza):

- Todo secreto (SECRET_KEY, credenciales de BD, host/usuario de SAP Service
  Layer) se lee de variables de entorno, nunca hardcodeado ni commiteado.
  `.env` está en .gitignore; `.env.example` documenta qué variables hacen falta.
- DEBUG es False por defecto; solo se activa explícitamente en desarrollo
  con DJANGO_DEBUG=True en el entorno local.
- Cookies de sesión y CSRF forzadas a HTTPS-only y HttpOnly en producción.
- HSTS, nosniff, X-Frame-Options DENY y política de referrer estricta
  activados cuando no se está en DEBUG.
- Validadores de contraseña completos de Django activos.
"""

from pathlib import Path

from decouple import Csv, config

BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------------
# Núcleo / secretos
# --------------------------------------------------------------------------

SECRET_KEY = config("DJANGO_SECRET_KEY")
DEBUG = config("DJANGO_DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", default="localhost,127.0.0.1", cast=Csv())

# --------------------------------------------------------------------------
# Aplicaciones
# --------------------------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",
    "control_points",
    "readings",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "qualitus_next.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "qualitus_next.wsgi.application"

# --------------------------------------------------------------------------
# Base de datos
#
# SQLite para desarrollo local (DATABASE_URL vacío). En producción se espera
# Postgres vía DATABASE_URL, p. ej.
# postgres://usuario:clave@host:5432/qualitus_next
# --------------------------------------------------------------------------

_database_url = config("DATABASE_URL", default="")
if _database_url:
    import dj_database_url

    DATABASES = {"default": dj_database_url.parse(_database_url, conn_max_age=600)}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# --------------------------------------------------------------------------
# Usuarios
# --------------------------------------------------------------------------

AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 12}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "control_points:list"
LOGOUT_REDIRECT_URL = "login"

# --------------------------------------------------------------------------
# Internacionalización
# --------------------------------------------------------------------------

LANGUAGE_CODE = "es"
TIME_ZONE = "Atlantic/Canary"
USE_I18N = True
USE_TZ = True

# --------------------------------------------------------------------------
# Archivos estáticos
# --------------------------------------------------------------------------

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --------------------------------------------------------------------------
# Endurecimiento de seguridad
#
# Todo esto se activa siempre que DEBUG sea False (es decir: en cualquier
# entorno que no sea desarrollo local explícito). No depende de recordar
# configurarlo aparte en producción.
# --------------------------------------------------------------------------

if not DEBUG:
    SECURE_SSL_REDIRECT = config("DJANGO_SECURE_SSL_REDIRECT", default=True, cast=bool)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = "same-origin"
    X_FRAME_OPTIONS = "DENY"

# Siempre activo, en DEBUG o no: las cookies de sesión y CSRF no deben ser
# legibles desde JavaScript.
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Sesión corta por inactividad: 8 horas, y se renueva en cada request.
SESSION_COOKIE_AGE = 60 * 60 * 8
SESSION_SAVE_EVERY_REQUEST = True

# --------------------------------------------------------------------------
# Integración con SAP Business One (Service Layer)
#
# El usuario ya tiene esta conexión funcionando en otros paneles; estas
# variables solo describen cómo este proyecto la consumirá cuando se
# conecte el acceso. No hay credenciales por defecto: si faltan, el cliente
# de Service Layer (sap/client.py, pendiente) debe fallar explícitamente en
# vez de intentar una conexión a medias.
# --------------------------------------------------------------------------

SAP_SERVICE_LAYER_BASE_URL = config("SAP_SERVICE_LAYER_BASE_URL", default="")
SAP_SERVICE_LAYER_COMPANY_DB = config("SAP_SERVICE_LAYER_COMPANY_DB", default="")
SAP_SERVICE_LAYER_USERNAME = config("SAP_SERVICE_LAYER_USERNAME", default="")
SAP_SERVICE_LAYER_PASSWORD = config("SAP_SERVICE_LAYER_PASSWORD", default="")
# Verificar TLS contra Service Layer siempre, salvo que se indique lo
# contrario explícitamente para un entorno de pruebas con certificado propio.
SAP_SERVICE_LAYER_VERIFY_TLS = config("SAP_SERVICE_LAYER_VERIFY_TLS", default=True, cast=bool)
