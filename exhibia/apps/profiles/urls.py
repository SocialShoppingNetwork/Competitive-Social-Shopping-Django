# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from functools import partial

from payments.models import Card
from shipping.forms import MemberInfoFormUS
from .forms import DeleteForm, BillingForm
from .views import manage_delete, manage_edit, manage_addresses
from .models import BillingAddress

urlpatterns = patterns("profiles.views",
    url(r'^$', 'account', {}, name="profile_account"),
    # url(r'^orders/(\w+)/$', 'checkout.views.view_order', {},
                        # name="checkout_view_order"),
    url(r'^shipping/$', 'manage_addresses', name="account_shipping"),
    url(r'^shipping/(?P<pk>\d+)/$', manage_edit, name="account_shipping_edit"),
    url(r'^shipping/delete/$', manage_delete,name="account_shipping_delete"),
    url(r'^billing/$', partial(manage_addresses, template='manage_billing.html',
                    user_attr='billing_addresses', form_class=MemberInfoFormUS), name="account_billing"),
    url(r'^billing/(?P<pk>\d+)/$', partial(manage_edit, model=BillingAddress,
                                redirect_url='account_billing', form=MemberInfoFormUS),
                         name="account_billing_edit"),
    url(r'^billing/delete/$', partial(manage_delete, model=BillingAddress, redirect_url='account_billing'),
                              name="account_billing_delete"),
    url(r'^payments/$', 'manage_payments', name="account_payments"),
    url(r'^payments/delete_card/$', partial(manage_delete, model=Card, redirect_url='account_payments'),
      name="account_delete_card"),
)
