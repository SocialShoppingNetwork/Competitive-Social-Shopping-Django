# -*- coding: utf-8 -*-

import pytest

from django.core.urlresolvers import reverse
from profiles.models import BillingAddress
from shipping.models import ShippingAddress
from payments.models import Card

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

def test_payments(logged_client):
    res = logged_client.get(reverse('account_payments'))
    assert res.status_code == 200

def test_payments_delete(logged_client):
    qs = Card.objects.filter(deleted=False)
    card_count = qs.count()
    res = logged_client.post(reverse('account_delete_card'), {'pk':qs[0].pk})
    assert res.status_code == 302
    assert card_count != qs.count()


@pytest.mark.parametrize(('model', 'url'), ((ShippingAddress, 'account_shipping_delete'),
             (BillingAddress, 'account_billing_delete')))
def test_address_delete(logged_client, user, model, url):
    qs = model.objects.filter(deleted=False, user=user)
    address_num = qs.count()
    res = logged_client.post(reverse(url),
                             {'pk':qs[0].pk})
    assert res.status_code == 302
    assert address_num != qs.count()

@pytest.mark.parametrize(('model', 'url'), ((ShippingAddress, 'account_shipping'),
             (BillingAddress, 'account_billing')))
def test_address_create(logged_client, user, model, url):
    qs = model.objects.filter(deleted=False, user=user)
    address_num = qs.count()
    res = logged_client.post(reverse(url),
                {'first_name':'test', 'last_name':'last name', 'address1':'address1',
                'address2':'address2','city':'some city', 'state':'AL',
                'country':'US','zip_code':'12345', 'phone':'123-456-7890', })
    assert res.status_code == 302
    assert address_num != qs.count(), 'not saved'


def test_deleting_get(logged_client):
    assert logged_client.get(reverse('account_billing_delete')).status_code == 404


@pytest.mark.parametrize(('url', 'model'), (
                         ('account_shipping_edit',ShippingAddress),
                         ('account_billing_edit', BillingAddress),))
def test_manage_edit(logged_client, url, model, user):
    address = model.objects.filter(user=user)[0]
    res = logged_client.get(reverse(url, kwargs={'pk':address.pk}))
    data = res.context['form'].initial
    data['first_name'] ='new first name'
    res = logged_client.post(reverse(url, kwargs={'pk':address.pk}), data)
    assert res.status_code == 302
    assert address.first_name != model.objects.get(pk=address.pk).first_name

