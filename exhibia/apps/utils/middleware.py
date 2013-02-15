__author__ = 'vh5'
class MemberMiddleware(object):
    def process_request(self, request):
        member = None
        if request.user.is_authenticated():
            try:
                member = request.user.get_profile()
            except: pass
        request.member = member
from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import ugettext as _


def basic_challenge(realm=None):
    if realm is None:
        realm = getattr(settings, 'WWW_AUTHENTICATION_REALM', _('Restricted Access'))
    # TODO: Make a nice template for a 401 message?
    response =  HttpResponse(_('Authorization Required'), mimetype="text/plain")
    response['WWW-Authenticate'] = 'Basic realm="%s"' % (realm)
    response.status_code = 401
    return response

def basic_authenticate(authentication):
    # Taken from paste.auth
    (authmeth, auth) = authentication.split(' ',1)
    if 'basic' != authmeth.lower():
        return None
    auth = auth.strip().decode('base64')
    username, password = auth.split(':',1)
    AUTHENTICATION_USERNAME = getattr(settings, 'BASIC_WWW_AUTHENTICATION_USERNAME')
    AUTHENTICATION_PASSWORD = getattr(settings, 'BASIC_WWW_AUTHENTICATION_PASSWORD')
    return username == AUTHENTICATION_USERNAME and password == AUTHENTICATION_PASSWORD

class BasicAuthenticationMiddleware(object):
    def process_request(self, request):
        if not getattr(settings, 'BASIC_WWW_AUTHENTICATION', False):
            return
        if 'HTTP_AUTHORIZATION' not in request.META:
            return basic_challenge()
        authenticated = basic_authenticate(request.META['HTTP_AUTHORIZATION'])
        if authenticated:
            return
        return basic_challenge()
