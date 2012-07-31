from django.http import *
from django.utils import simplejson
from django.conf import settings
from time import time

class PaymentVerificationFailed(Exception):
    pass

class UnsupportedNotification(Exception):
    pass

class PaymentGateway(object):
    
    def __init__(self, merchant):
        self.merchant = merchant
        self.fields = {}
    
    def call(self, request, data, handler, extra=None, must_verify=True):
        self.data = data
        self.handler = handler
        self.extra = extra
        self.request = request
        logfile_dir = os.path.dirname(os.path.abspath(__file__))
        self.logfile = os.path.abspath(os.path.join(logfile_dir, 'log/%s-%i.txt' % (self.__class__.__name__.lower(), int(time()*1000))))       

        #if settings.PAYMENTS_LOG:
        #    self.log()

        self.pn = self.create_payment_notification()        
        
        if must_verify:
            if self.verify():
                r = self.process()
            else:                
                raise PaymentVerificationFailed
        else:
            r = self.process()

        if r:
            return r
        else:
            return self.default_response()
        
    def log(self):
        fh = open(self.logfile, 'w')
        fh.write(str(self.request))
        fh.close()
    """
    def get_url(self):
        pass"""

    def verify(self):
        pass        
    
    def create_payment_notification(self):
        pass
    
    def process(self):
        return self.handler(self.request, self.data, self.pn, self.extra)

    def default_response(self, msg='OK'):
        return HttpResponse(msg)

def hopHash(data, key):
    import base64, hmac
    try: 
        import hashlib 
        sha_constructor = hashlib.sha1
    except ImportError: 
        import sha
        sha_constructor = sha
    return base64.b64encode(hmac.HMAC(key, data, digestmod=sha_constructor).digest())

"""
WARNING: handler raise exception problem

if we raise exception during the callback process
usually the payment gateway will continue send it
better log it, and return 200
"""
