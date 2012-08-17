from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("checkout.views",
    url(r"^select-shipping-address/(\d+)/$", "select_shipping_address", name="checkout_select_shipping_address"),
    url(r"^select-billing-address/(\d+)/$", "select_billing", name="checkout_select_billing"),
    url(r"^select-shipping/(\d+)/$", "select_shipping", name="checkout_select_shipping"),
    url(r"^select-payment/(\d+)/$", "select_payment", name="checkout_select_payment"),
    url(r"^review/(\d+)/$", "review_order", name="checkout_review"),
    url(r"^request/(\d+)/$", "request_shipping_fee", name="checkout_request_fee"),
)
