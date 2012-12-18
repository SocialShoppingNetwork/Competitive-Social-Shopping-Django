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
    print client.login(username=user.username, password='IMLpYcUPIUzUA')
    return client
