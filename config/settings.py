import os
from pathlib import Path

import dj_database_url
from django.conf.global_settings import gettext_noop
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

MODE = os.getenv("MODE")

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = True if MODE == "dev" else False

ALLOWED_HOSTS = ["*"]

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "drf_yasg",
    "rest_framework",
]

if DEBUG:
    DJANGO_APPS += [
        "silk",
    ]

LOCAL_APPS = [
    "common",
    "authentication",
    "jobs",
    "users",
]


INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    MIDDLEWARE += [
        "silk.middleware.SilkyMiddleware",
    ]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Rest Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DATABASE_URL = os.getenv("DATABASE_URL")
DATABASES = {"default": dj_database_url.config(default=DATABASE_URL)}


AUTH_USER_MODEL = "authentication.AuthUser"


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.authentication.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.authentication.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.authentication.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.authentication.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/
LANGUAGE_CODE = "en-us"

LANGUAGES = (
    ("ko", gettext_noop("Korean")),
    ("en", gettext_noop("English")),
    ("vi", gettext_noop("Vietnamese")),
)

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
