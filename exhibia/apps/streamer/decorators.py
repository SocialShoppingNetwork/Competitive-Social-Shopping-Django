# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

def login_required(method):
    def wraps(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            self.emit("AUTH_REQUIRED", reverse('acct_login'))
            return
        return method(self, *args, **kwargs)
    return wraps
