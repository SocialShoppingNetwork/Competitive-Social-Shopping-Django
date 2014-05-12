# -*- coding: utf-8 -*-
# Django settings for basic pinax project.
from os import environ, path
import posixpath
import pinax

PINAX_ROOT = path.abspath(path.dirname(pinax.__file__))
PROJECT_ROOT = path.dirname(path.abspath(path.dirname(__file__)))

# tells Pinax to use the default theme
PINAX_THEME = "default"


DEBUG = True
TEMPLATE_DEBUG = DEBUG

# tells Pinax to serve media through the staticfiles app.
SERVE_MEDIA = False


ADMINS = [
    # ("Your Name", "your_email@domain.com"),
]

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'f1398afa8bfa20dbd6efefe4106a86aad5c683b2.rackspaceclouddb.com',
        'USER': 'exhibia',
        'PASSWORD': '$$nrule2020',
        'NAME': 'exhibia'
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "US/Eastern"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = path.join(PROJECT_ROOT, "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
# MEDIA_URL = "/site_media/static/media/"
MEDIA_URL = "/media/"

# Absolute path to the directory that holds static files like app media.
# Example: "/home/media/media.lawrence.com/apps/"
STATIC_ROOT = path.join(PROJECT_ROOT, "static")

# URL that handles the static files like app media.
# Example: "http://media.lawrence.com"
# STATIC_URL = "http://s3.amazonaws.com/ssn-network/"
STATIC_URL = "http://static.exhibia.com/"
# STATIC_URL = "/static/"

# Additional directories which hold static files
STATICFILES_DIRS = [
    #path.join(PINAX_ROOT, "themes", PINAX_THEME, "static"),
]

STATICFILES_FINDERS = [
    "staticfiles.finders.FileSystemFinder",
    "staticfiles.finders.AppDirectoriesFinder",
    "staticfiles.finders.LegacyAppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = posixpath.join(STATIC_URL, "admin/")


# Make this unique, and don't share it with anybody.
SECRET_KEY = "y(si0o6#r6@b87d24!(dl=9pe23b*b@tobc(x$()@1#q)4ds-u"

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.gzip.GZipMiddleware',

    # 'tracking.middleware.BannedIPMiddleware',

    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_openid.consumer.SessionConsumer",

    # 'tracking.middleware.VisitorTrackingMiddleware',

    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
    "pinax.apps.account.middleware.LocaleMiddleware",
    "pagination.middleware.PaginationMiddleware",
    "pinax.middleware.security.HideSensistiveFieldsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "utils.middleware.MemberMiddleware",
    "utils.middleware.BasicAuthenticationMiddleware",
    "referrals.middlewares.RefererMiddleware",
    # 'tracking.middleware.VisitorCleanUpMiddleware',
]

ROOT_URLCONF = "exhibia.urls"

TEMPLATE_DIRS = [
    path.join(PROJECT_ROOT, "templates"),
    path.join(PINAX_ROOT, "themes", PINAX_THEME, "templates"),
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",

    "staticfiles.context_processors.static",

    "pinax.core.context_processors.pinax_settings",

    "pinax.apps.account.context_processors.account",

    "notification.context_processors.notification",
    "announcements.context_processors.site_wide_announcements",

    "profiles.context_processors.member",
    "utils.context_processors.settings",
    'social_auth.context_processors.social_auth_by_name_backends',
    'social_auth.context_processors.social_auth_login_redirect',
]


INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.humanize",
    "django.contrib.flatpages",
    "django.contrib.staticfiles",

    "pinax.templatetags",

    # external
    "notification", # must be first
    "staticfiles",
    "compressor",
    "debug_toolbar",
    "mailer",
    "uni_form",
    "django_openid",
    "timezones",
    "emailconfirmation",
    "announcements",
    "pagination",
    "south",
    "tinymce",
    'cumulus',
    "social_auth",
    "django_countries",
    # Pinax
    "pinax.apps.account",
    "pinax.apps.signup_codes",
    #"pinax.apps.analytics",fa
    "crispy_forms",
    "easy_thumbnails",
    "gunicorn",
    "storages",
    # 'tracking',
    'dbsettings',

    # project
    "about",
    "profiles",
    "auctions",
    "testimonials",
    "bidin",
    #"matic",
    "utils",
    "payments",
    "shipping",
    "checkout",
    # ndevs apps
    "socials",
    'referrals',
    'streamer',
    'points_store'

]

TEST_RUNNER = 'coverage_runner.CaverageTestSuiteRunner'
COVERAGE_REPORT_PATH = path.join(PROJECT_ROOT, 'coverage_report')
FIXTURE_DIRS = [
    path.join(PROJECT_ROOT, "fixtures"),
]

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

EMAIL_BACKEND = "mailer.backend.DbBackend"

ABSOLUTE_URL_OVERRIDES = {
    "auth.user": lambda o: "/profiles/profile/%s/" % o.username,
}

AUTH_PROFILE_MODULE = "profiles.Member"
NOTIFICATION_LANGUAGE_MODULE = "account.Account"


AUTHENTICATION_BACKENDS = [
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    #"pinax.apps.account.auth_backends.AuthenticationBackend",
    'social_auth.backends.twitter.TwitterBackend',
    "django.contrib.auth.backends.ModelBackend",
]

LOGIN_URL = "/account/login/" # @@@ any way this can be a url name?
LOGIN_REDIRECT_URLNAME = "home"

EMAIL_CONFIRMATION_DAYS = 2
EMAIL_DEBUG = DEBUG

COMPRESS_URL = STATIC_URL

# temporary unable memcahe
# environ['MEMCACHE_SERVERS'] = environ.get('MEMCACHIER_SERVERS', '')
# environ['MEMCACHE_USERNAME'] = environ.get('MEMCACHIER_USERNAME', '')
# environ['MEMCACHE_PASSWORD'] = environ.get('MEMCACHIER_PASSWORD', '')
# environ['MEMCACHE_SERVERS'] = "mc2.ec2.memcachier.com:11211"
# environ['MEMCACHE_USERNAME'] = "237cfc"
# environ['MEMCACHE_PASSWORD'] = "c8442b7942494c9f54c0"
#
# CACHES = {
#     'default': {
#         'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
#         'LOCATION': environ.get('MEMCACHIER_SERVERS', ''),
#         'TIMEOUT': 500,
#         'BINARY': True,
#         'KEY_PREFIX': 'bidstick',
#     },
# }


# SESSION_ENGINE = "django.contrib.sessions.backends.bidomaticcache"
SESSION_COOKIE_AGE = 15552000

# SOCKETIO_SERVER = 'powerful-taiga-2596.herokuapp.com'
SOCKETIO_SERVER = 'exhibia.com'

SITE_NAME = 'testing.exhibia.com'

REDIS = {
    'username': 'root',
    'password': '',
    'host': 'localhost',
    'port': 6379,
}


MONGO = {
    'username': 'root',
    'password': '',
    'host': 'localhost',
    'port': 27017,
}

# geoip
GEOIP_PATH = path.join(path.dirname(PROJECT_ROOT), 'geoip')
TRACKING_USE_GEOIP = True

BASIC_WWW_AUTHENTICATION_USERNAME = "admin"
BASIC_WWW_AUTHENTICATION_PASSWORD = "admin"
BASIC_WWW_AUTHENTICATION = False

try:
    from .local_settings import *
except ImportError:
    pass
