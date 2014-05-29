from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
    url(r'^paypal_buy_now/$', 'payments.views.paypal_buy_now'),
    url(r'^paypal_buy_bids/$', 'payments.views.paypal_buy_bids'),
)