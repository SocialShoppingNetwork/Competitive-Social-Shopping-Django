# -*- coding: utf-8 -*-

import pytest

from django.core.urlresolvers import reverse
from profiles.models import BillingAddress
from shipping.models import ShippingAddress

def test_login(client, django_settings):
    login_page = client.get(reverse('acct_login'))
    assert login_page.status_code == 200

    login = client.post(reverse('acct_login'), {'username':'test',
                        'password':django_settings.TEST_USER_PASSWORD})
    assert login.status_code == 302
    assert not login.context
    assert 'sessionid' in login.cookies.keys()


def test_account_main_view(logged_client):
    res = logged_client.get(reverse('profile_account'))
    assert res.status_code == 200
    assert len(res.context['auctions_waiting_payment'])


def test_shipping(logged_client):
    res = logged_client.get(reverse('account_shipping'))
    assert res.status_code == 200

def test_billing(logged_client):
    res = logged_client.get(reverse('account_billing'))
    assert res.status_code == 200


@pytest.mark.parametrize(('model', 'url'), ((ShippingAddress, 'account_shipping_delete'),
             (BillingAddress, 'account_billing_delete')))
def test_address_delete(logged_client, user, model, url):
    qs = model.objects.filter(deleted=False, user=user)
    address_num = qs.count()
    res = logged_client.post(reverse(url),
                             {'pk':qs[0].pk})
    assert res.status_code == 302
    assert address_num != qs.count()

@pytest.mark.parametrize(('model', 'url'), ((ShippingAddress, 'account_shipping_delete'),
             (BillingAddress, 'account_billing_delete')))
def test_address_create(logged_client, user, model, url):
    qs = ShippingAddress.objects.filter(deleted=False, user=user)
    address_num = qs.count()
    res = logged_client.post(reverse('account_shipping'),
                {'first_name':'test', 'last_name':'last name', 'address1':'address1',
                'address2':'address2','city':'some city', 'state':'some_state',
                'country':'US','zip_code':'123', 'phone':'123456789'})
    assert res.status_code == 302
    assert address_num != qs.count()

