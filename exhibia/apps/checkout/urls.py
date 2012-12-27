# -*- coding: utf-8 -*-

from functools import partial
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

from profiles.views import AddressView, CardCreateView
from profiles.models import BillingAddress

# this should be deleted
# urlpatterns = patterns("checkout.views",
#     url(r"^select-shipping-address/(\d+)/$", "select_shipping_address", name="checkout_select_shipping_address"),
#     url(r"^select-billing-address/(\d+)/$", "select_billing", name="checkout_select_billing"),
#     url(r"^select-shipping/(\d+)/$", "select_shipping", name="checkout_select_shipping"),
#     url(r"^select-payment/(\d+)/$", "select_payment", name="checkout_select_payment"),
#     url(r"^review/(\d+)/$", "review_order", name="checkout_review"),
#     url(r"^request/(\d+)/$", "request_shipping_fee", name="checkout_request_fee"),
#     url(r"^create_order/(?P<auction_pk>\d+?)/(?P<address_pk>\d+?)/$", 'select_shipping_address', name='create_order')
# )

urlpatterns = patterns('',
    url(r"^shipping/(?P<auction_pk>\d+?)/$", AddressView.as_view(choose_address=True,
                            headline="Select your shipping address"), name='checkout_shipping'),
    url(r"^billing/(?P<auction_pk>\d+?)/(?P<shipping_pk>\d+?)/$",
            AddressView.as_view(headline="Select your billing address", choose_address=True, model=BillingAddress),
            name='checkout_billing'),
    url(r"^payment/(?P<auction_pk>\d+?)/(?P<shipping_pk>\d+?)/(?P<billing_pk>\d+?)/$",
                CardCreateView.as_view(choose_card=True, headline="Choose your payment method"),
                 name='checkout_payment'),
    url(r"^confirm_order/(?P<auction_pk>\d+?)/(?P<shipping_pk>\d+?)/(?P<billing_pk>\d+?)/(?P<card_pk>\d+?)/$",
                    "checkout.views.confirm_order", name="checkout_confirm_order"),
    url(r"^review/(?P<order_pk>\d+?)/$", "checkout.views.view_order", name="checkout_review_order"),
)
