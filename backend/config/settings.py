"""
Configuration du projet Django - Portfolio de Lazaki Chelsoube
Version compatible Render (production) et local (développement).
"""
import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

# Render définit automatiquement la variable RENDER=true
IS_RENDER = bool(os.environ.get('RENDER'))

# --- SECURITE -----------------------------------------------------------
# En local : DEBUG=True par défaut. Sur Render : DEBUG=False par défaut.
DEBUG = os.environ.get('DEBUG', 'False' if IS_RENDER else 'True') == 'True'

# Sur Render, définissez SECRET_KEY dans Environment (Dashboard).
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    if IS_RENDER and not DEBUG:
        raise ImproperlyConfigured(
            "La variable d'environnement SECRET_KEY est obligatoire en production."
        )
    SECRET_KEY = 'django-insecure-cle-de-developpement-uniquement'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Nom d'hôte fourni automatiquement par Render (ex: portfolio-lazaki.onrender.com)
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Domaine explicite (utile si le nom Render change ou avec un domaine perso)
ALLOWED_HOSTS.append('portfolio-lazaki.onrender.com')

CSRF_TRUSTED_ORIGINS = ['https://portfolio-lazaki.onrender.com']
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f'https://{RENDER_EXTERNAL_HOSTNAME}')

# Render est derrière un proxy HTTPS
if IS_RENDER:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# --- APPLICATIONS ---------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps tierces
    'rest_framework',
    'corsheaders',

    # App du portfolio
    'portfolio',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # doit rester tout en haut
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # juste après SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# --- BASE DE DONNEES ------------------------------------------------------
# Si DATABASE_URL est défini (PostgreSQL Render), on l'utilise.
# Sinon : SQLite (attention, le disque de Render est éphémère :
# la base SQLite est réinitialisée à chaque redéploiement).
if os.environ.get('DATABASE_URL'):
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- INTERNATIONALISATION ---------------------------------------------
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Dakar'
USE_I18N = True
USE_TZ = True

# --- FICHIERS STATIQUES ET MEDIA --------------------------------------
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- DJANGO REST FRAMEWORK ------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# --- CORS ------------------------------------------------------------------
# Développement : tout est autorisé.
# Production : uniquement les origines listées dans la variable
# d'environnement CORS_ALLOWED_ORIGINS (séparées par des virgules), ex :
#   https://mon-frontend.onrender.com,https://mondomaine.com
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = [
        o.strip()
        for o in os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
        if o.strip()
    ]