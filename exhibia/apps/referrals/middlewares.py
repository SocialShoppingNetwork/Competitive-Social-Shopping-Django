# -*- coding: utf-8 -*-

from urlparse import urlparse

from django.contrib.sites.models import Site

class RefererMiddleware(object):

    domains = set(Site.objects.all().values_list('domain', flat=True))

    def process_request(self, request):
        if not request.user.is_authenticated():
            netloc = urlparse(request.META.get('HTTP_REFERER', '')).netloc
            if netloc and netloc not in self.domains:
                request.session['ref'] = netloc
