from common_settings import *

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql_psycopg2", # Add "postgresql_psycopg2", "postgresql", "mysql", "sqlite3" or "oracle".
        "NAME": "exhibia",                       # Or path to database file if using sqlite3.
        "USER": "vh5",                             # Not used with sqlite3.
        "PASSWORD": "",                         # Not used with sqlite3.
        "HOST": "localhost",                             # Set to empty string for localhost. Not used with sqlite3.
        "PORT": "",                             # Set to empty string for default. Not used with sqlite3.
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': ['localhost:11211'],
        'TIMEOUT': 60,
        'KEY_PREFIX': 'bidstick'
    }
}

SOCKETIO_SERVER = '%s:4000' % (SITE_NAME)

