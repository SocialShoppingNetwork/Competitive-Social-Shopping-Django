# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('points_store.views',
        url(r"^$", 'store_list', name="points_store_index")
   )
