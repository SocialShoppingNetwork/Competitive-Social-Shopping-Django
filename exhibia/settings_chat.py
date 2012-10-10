from settings import *

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.humanize",

    "pinax.templatetags",

    # external
    "staticfiles",
    "compressor",
    "timezones",
    "pagination",
    # Pinax
    "pinax.apps.account",
    "gunicorn",

    'django_socketio',

    # project
    "about",
    "profiles",
    "utils",
    # ndevs apps
    "socials",
    "social_auth",
]

