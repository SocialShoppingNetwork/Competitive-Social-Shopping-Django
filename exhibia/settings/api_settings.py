# -*- coding: utf-8 -*-

#payments
TEST_MODE = True
PLIMUS_CALL_URL='https://%s.plimus.com/jsp/buynow.jsp' % (TEST_MODE and 'sandbox' or 'www')
PAYMENTS_LOG = True
PAYMENTS_GATEWAY = ('plimus', 'dalpay')

DALPAY_CALL_URL = 'https://secure.dalpay.is/cgi-bin/order2/processorder1.pl'
DALPAY_MERCHANT_ID = '120205'

TWITTER_CONSUMER_KEY         = 'y2vUwX1Bsamx9X8wYmM9g'
TWITTER_CONSUMER_SECRET      = 'LvavS6nKMrzG8wMm6feah84lnMxOXb6e9mKVrf09Pg'
TWITTER_ACCESS_TOKEN = ''
TWITTER_TOKEN_SECRET = ''
TWITTER_HASH_TAGS = ['exhibia']

LOGIN_URL          = '/account/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL    = '/login-error/'


#GOOGLE_OAUTH2_CLIENT_KEY     = '33411447270.apps.googleusercontent.com'
#GOOGLE_OAUTH2_CLIENT_SECRET  = '2M0KMp0uMUfdjX0XbtORhQ-i2'
#GOOGLE_OAUTH_EXTRA_SCOPE = ['http://gdata.youtube.com']


#video-manager
VIDEO_MANAGER_CONFIG = {
    'DEVELOPER_KEY': 'AI39si4mlBv42cQbZOPyMaFtMBu-X2M1Uikq_pyoST-Wf1L32jll00nkVq9hXWhZIJNt6ZqoZlBfEBUnwU_Z7RUTkki-3RSH2g',
    'CLIENT_ID': 'Bidstick',
    'SOURCE':'django_video_rec',
    'VIDEO_PATH': 'videos',
    'VIDEO_SAVE_FN': 'testimonials.views.video_save_fn',
    'VIDEO_SNAPSHOT_FN': 'testimonials.views.video_snapshot_fn',
    'VIDEO_ID_FN': 'testimonials.views.video_id_fn',
    'RTMP_SERVER': 'rtmp://test.app.com/hdfvr/_definst_'
}
#from django.core.files.storage import default_storage
#default_storage.path('fichero.flv')

SOCIAL_ACCOUNTS = {
    'youtube': {
        'DEVELOPER_KEY': 'AI39si4mlBv42cQbZOPyMaFtMBu-X2M1Uikq_pyoST-Wf1L32jll00nkVq9hXWhZIJNt6ZqoZlBfEBUnwU_Z7RUTkki-3RSH2g',
        'CLIENT_ID': 'Bidstick',
        'SOURCE':'django_video_rec',
        'USERNAME': 'xtealc@gmail.com',
        'PASSWORD': ''
    },
    'facebook': {
        'API_ID': '129299757101755',
        'API_SECRET': '6b2f92a905b24bbc762c20c37c7cd7df',
        'ACCESS_TOKEN': 'AAABphjOSYt8BAPE8uSe7WiwZC6616gJwGqwoLdKi8QFRZANft2i8vqfzN1UZBoS4x7zNbNNfQWlqmZAU40Ktdzd1YYZCE1TEZD',
        'PAGE_ID': '107701282676058',
        'PAGE_ACCESS_TOKEN': 'AAABphjOSYt8BAKCkjVrybJQXqV6hJIPZBPdqoZB1jksCoYLFZAlJ9CXP5NADQphbePwW1CP9ZCoHuTbQYI5MGZAgqMeCo0nchlSPxLGWE7AZDZD'
    }
}

RED5_STREAM_PATH = '/Users/vh5/Downloads/hd/red8/webapps/hdfvr/streams/_definst_/'

# Social

GOOGLEPLUS_ITEM_LIMIT_DAILY = 2
GOOGLEPLUS_ITEM_FREEBIDS = 1
FACEBOOK_LIKES_ITEM_LIMIT_DAILY = 2
FACEBOOK_LIKE_ITEM_FREEBIDS = 1

# endSocial


FACEBOOK_APP_ID              = '129299757101755'
FACEBOOK_API_SECRET          = '6b2f92a905b24bbc762c20c37c7cd7df'
FACEBOOK_EXTENDED_PERMISSIONS = ['email']

GOOGLE_OAUTH2_CLIENT_ID = '313089854027-tfljmmcdf9bt0b07bqo23dj9o7q231d2.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'esTgrmFueFCC3HzF9KnMdRQK'

#FACEBOOK_AUTH_EXTRA_ARGUMENTS = {'display': 'popup'}

SOCIAL_AUTH_CREATE_USERS = True
#SOCIAL_AUTH_FORCE_RANDOM_USERNAME = False
SOCIAL_AUTH_DEFAULT_USERNAME = 'socialauth_user'

LOGIN_REDIRECT_URL = '/'
