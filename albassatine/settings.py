# Django settings
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = 'django-insecure-change-this-key'

DEBUG = False


ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'boucherie-albassatine.ma', 'www.boucherie-albassatine.ma']


# Installed applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your application
    'boucherie',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'albassatine.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # Si tu gardes tous les templates dans boucherie/templates,
        # laisse DIRS vide.
        'DIRS': [],

        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'albassatine.wsgi.application'


# ======================================================
# DATABASE (MySQL)
# ======================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'albassatine_db',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Language
LANGUAGE_CODE = 'fr'

TIME_ZONE = 'Africa/Casablanca'

USE_I18N = True

USE_TZ = True

# ======================================================
# STATIC FILES
# ======================================================
# NOTE : STATICFILES_DIRS a été retiré. Django détecte déjà
# automatiquement le dossier "static/" de l'app "boucherie"
# (boucherie/static/). Le garder en plus créait des chemins
# en double detectés deux fois par collectstatic (le warning
# "Found another file with the destination path ...").
#
# Si un jour tu as un dossier de statics GLOBAL (hors d'une
# app précise, ex: BASE_DIR / 'static'), remets STATICFILES_DIRS
# en pointant uniquement vers CE dossier-là (pas boucherie/static).

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise : sert correctement les fichiers statiques même
# avec DEBUG = False, en local (runserver) comme en production.
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ======================================================
# MEDIA FILES
# ======================================================

MEDIA_URL = 'media/'

MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'boucheriealbassatine@gmail.com'
EMAIL_HOST_PASSWORD = 'gfdn eqna hsth dimm'
DEFAULT_FROM_EMAIL = 'AL BASSATINE VIANDES <boucheriealbassatine@gmail.com>'

# Adresse qui reçoit les notifications du formulaire de contact du site.
# (peut être différente de DEFAULT_FROM_EMAIL si tu veux un jour rediriger
# vers un autre email, ex: le responsable commercial)
CONTACT_NOTIFY_EMAIL = 'boucheriealbassatine@gmail.com'