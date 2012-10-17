# -*- coding: utf-8 -*-
import os

# debug toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]

def show_toolbar(request):
    if 'HEROKU' in os.environ:
        if not request.user.is_superuser:
            return False
    return True

DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
    "TAG":'head',
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
}


# custom apps settings
PRICE_INTERVAL = 0.01
MAX_AUCTIONS = 12
MAX_TIME_HOMEPAGE = 30


PLEDGE_TIME = 180


# auth

ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_REQUIRED_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = False
ACCOUNT_EMAIL_AUTHENTICATION = False
ACCOUNT_UNIQUE_EMAIL = EMAIL_CONFIRMATION_UNIQUE_EMAIL = False


TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,spellchecker,paste,searchreplace",
    'theme': "advanced",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
    'width' : '768',
    'height':'512',
    }

# storages
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = 'AKIAJCAXW2LKY2RXOFAA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'exhibia'
AWS_PRELOAD_METADATA = True

# django-compressor
COMPRESS = True
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_HEADERS = {
    'Expires': 'Sun, 19 Jul 2020 18:06:32 GMT'
}

