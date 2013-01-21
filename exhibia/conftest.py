# -*- coding: utf-8 -*-

import sys, os
import pytest

from django.core.management import call_command

SETTINGS_MODULE_ENV = 'settings'
curdir = os.path.realpath(os.curdir)
apps_dir = os.path.join(curdir,'apps')
if apps_dir not in sys.path:
    sys.path.insert(0, apps_dir)

if curdir not in sys.path:
    sys.path.insert(0, curdir)


pytest_plugins=['cov']

def pytest_configure():
    print 'running load db'
    from django.contrib.auth.models import User
    if not User.objects.count():
        call_command('loaddata', 'dev')

from django.http import HttpRequest
from django.contrib.auth import login
from django.utils.importlib import import_module

@pytest.fixture()
def logged_client(client, user, settings):
    # client.login(username=user.username, password='IMLpYcUPIUzUA')
    request = HttpRequest()
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    if client.session:
        request.session = client.session
    else:
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
    login(request, user)

    # Save the session values.
    request.session.save()

    # Set the cookie to represent the session.
    session_cookie = settings.SESSION_COOKIE_NAME
    client.cookies[session_cookie] = request.session.session_key
    cookie_data = {
        'max-age': None,
        'path': '/',
        'domain': settings.SESSION_COOKIE_DOMAIN,
        'secure': settings.SESSION_COOKIE_SECURE or None,
        'expires': None,
    }
    client.cookies[session_cookie].update(cookie_data)
    return client

@pytest.fixture(scope='session')
def finished_auction(user):
    from auctions.models import Auction
    return Auction.objects.finished().get(last_bidder_member=user)

@pytest.fixture(scope='session')
def shipping_address(user):
    from shipping.models import ShippingAddress
    return ShippingAddress.objects.filter(user=user)[0]

@pytest.fixture(scope='session')
def billing_address(user):
    from profiles.models import BillingAddress
    return BillingAddress.objects.filter(user=user)[0]

@pytest.fixture(scope='session')
def card(user):
    from payments.models import Card
    return Card.objects.filter(user=user)[0]
