# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse

class ReferralLink(models.Model):

    user = models.ForeignKey(User, related_name='refferal_urls')
    redirect_to = models.CharField(max_length=500, default='/')
    visit_count = models.PositiveIntegerField(default=0)
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now)

    @models.permalink
    def get_absolut_url(self):
        return 'refferal_url', (), {'referral_link':self.pk}

    def __unicode__(self):
        return u'refferal for %s' % self.user
