# -*- coding: utf-8 -*-

import os

from django.db import models
from django.conf import settings

from tinymce.models import HTMLField

def upload_to(instance, filename):
    return u'point_store/%s' % filename


class StoreItem(models.Model):

    type_choices = (
            (1, 'Win limit'),
            (2, 'Autobidder')
                    )

    item_type = models.PositiveSmallIntegerField(choices=type_choices)
    cost = models.PositiveSmallIntegerField(help_text=u"number of points this item cost")
    duration = models.PositiveIntegerField(help_text=u'How long this item will be active after buy in hours')
    description = HTMLField()
    image = models.ImageField(upload_to=upload_to, default=os.path.join(settings.PROJECT_ROOT, 'images/super-man-icon.png'))
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s lasts - %s, cost - %s' %(self.item_type, self.duration, self.cost)

class BoughtItem(models.Model):

    user = models.ForeignKey('auth.user')
    item = models.ForeignKey(StoreItem, related_name='bought')
    bought_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s - %s'% (self.user, self.item )
