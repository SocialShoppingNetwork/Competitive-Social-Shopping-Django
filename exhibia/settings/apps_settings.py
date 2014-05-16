# -*- coding: utf-8 -*-
import os
from decimal import Decimal
# CLOUD_ID_TYPE=rackspace
# debug toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]

DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
    "TAG":'head',
    'SHOW_TOOLBAR_CALLBACK': False,
}


# custom apps settings
PRICE_INTERVAL = Decimal(0.01)
MAX_AUCTIONS = 25
MIN_ACTIVE_AUCTIONS = 5
MAX_TIME_HOMEPAGE = 30


PLEDGE_TIME = 180
SHOWCASE_TIME = 3600

# delay before displaying for bidding (after item was fully funded)
TRANSITION_PHASE_1_TIME = 0.2 * 60
# item will stay there for X mins more displaying the winner until disappears from bidding and appears to funding
TRANSITION_PHASE_2_TIME = 1 * 60


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

### rackspace cloud files settings
CLOUDFILES_USERNAME = 'artem.davidov'
CLOUDFILES_API_KEY = '2f7bfec9dc1b45e09bbccfb318dfd4b8'
CLOUDFILES_CONTAINER = 'static'
DEFAULT_FILE_STORAGE = 'storages.backends.mosso.CloudFilesStorage'
# Optional - use SSL
#CLOUDFILES_SSL = True


# django-compressor
# COMPRESS = False
# COMPRESS_ENABLED = False
# COMPRESS = True
# COMPRESS_ENABLED = True
# COMPRESS_OFFLINE = True
# COMPRESS_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
# COMPRESS_STORAGE = 'storages.backends.mosso.CloudFilesStorage'

max_age = 315360000 # year

# notification broadcast
AUTOMESSAGE_DELAY = 60 * 5 # every 5 minutes
