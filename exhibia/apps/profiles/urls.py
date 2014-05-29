# -*- coding: utf-8 -*-

from functools import partial

from django.conf.urls.defaults import *

from social_auth.views import auth, complete, disconnect

from payments.models import Card
from shipping.forms import MemberInfoFormUS
from .forms import DeleteForm, BillingForm
from .views import manage_delete, manage_edit, AddressView, CardCreateView
from .models import BillingAddress

urlpatterns = patterns("profiles.views",
    url(r'^$', 'account', {}, name="profile_account"),
    # url(r'^orders/(\w+)/$', 'checkout.views.view_order', {},
                        # name="checkout_view_order"),
    url(r'^shipping/$', AddressView.as_view(headline="Manage your shipping address"), name="account_shipping"),
    url(r'^shipping/(?P<pk>\d+)/$', manage_edit, name="account_shipping_edit"),
    url(r'^shipping/delete/$', manage_delete,name="account_shipping_delete"),
    url(r'^billing/$', AddressView.as_view(headline="Manage your billing address",
                                           model=BillingAddress),
                             name="account_billing"),
    url(r'^billing/(?P<pk>\d+)/$', partial(manage_edit, model=BillingAddress,
                                redirect_url='account_billing', form=MemberInfoFormUS),
                         name="account_billing_edit"),
    url(r'^billing/delete/$', partial(manage_delete, model=BillingAddress, redirect_url='account_billing'),
                              name="account_billing_delete"),
    url(r'^payments/$', CardCreateView.as_view(), name="account_payments"),
    url(r'^payments/delete_card/$', partial(manage_delete, model=Card, redirect_url='account_payments'),
      name="account_delete_card"),
)


urlpatterns += patterns('',
    url(r'^points_store/', include('points_store.urls')),
    # authentication
    url(r'^account/login/$', 'django.contrib.auth.views.login'),
    url(r'^login/(?P<backend>[^/]+)/$', auth,
        name='socialauth_begin'),
    url(r'^complete/(?P<backend>[^/]+)/$', 'socials.views.registration_complete',
        name='socialauth_complete'),

    # disconnection
    url(r'^disconnect/(?P<backend>[^/]+)/$', disconnect,
        name='socialauth_disconnect'),
    url(r'^disconnect/(?P<backend>[^/]+)/(?P<association_id>[^/]+)/$',
        disconnect, name='socialauth_disconnect_individual'),
)
