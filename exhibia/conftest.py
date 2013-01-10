# -*- coding: utf-8 -*-

import sys, os
import pytest

from django.core.management import call_command


curdir = os.path.realpath(os.curdir)
apps_dir = os.path.join(curdir,'apps')
if apps_dir not in sys.path:
    sys.path.insert(0, apps_dir)

if curdir not in sys.path:
    sys.path.insert(0, curdir)


pytest_plugins=['pydjango', 'cov']

def pytest_configure():
    print 'running load db'
    from django.contrib.auth.models import User
    if not User.objects.count():
        call_command('loaddata', 'dev')


@pytest.fixture()
def logged_client(client, user):
    client.login(username=user.username, password='IMLpYcUPIUzUA')
    return client

@pytest.fixture()
def finished_auction(user):
    from auctions.models import Auction
    return Auction.objects.finished().get(last_bidder_member=user)

@pytest.fixture()
def shipping_address(user):
    from shipping.models import ShippingAddress
    return ShippingAddress.objects.filter(user=user)[0]

@pytest.fixture()
def billing_address(user):
    from profiles.models import BillingAddress
    return BillingAddress.objects.filter(user=user)[0]

@pytest.fixture()
def card(user):
    from payments.models import Card
    return Card.objects.filter(user=user)[0]
