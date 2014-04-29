# -*- coding: utf-8 -*-
import os

from .general_settings import *
from .apps_settings import *
from .api_settings import *
from .test_settings import *
# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
# on_heroku = 'HEROKU' in os.environ
# if not on_heroku:
#     try:
#         from .local_settings import *
#     except ImportError:
#         pass
