# -*- coding: utf-8 -*-

from fabric.api import local as _

def deploy():
    _('git push')
    _('heroku maintenance:on')

    _('git push heroku master')
    _('heroku run python exhibia/manage.py syncdb --noinput')
    _('heroku run python exhibia/manage.py migrate')
    _('heroku run python exhibia/manage.py loaddata dev')

    _('heroku maintenance:off')
