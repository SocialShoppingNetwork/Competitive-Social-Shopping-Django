__author__ = 'airam'

from django.conf.urls.defaults import *
from django.conf import settings

from social_login.forms import SignupForm


urlpatterns = patterns("social_login.views",
    url(r'^account/login/callback/$', 'callback', name='login-callback'),
    url(r'^account/login/error/$', 'error', name='login-error'),
    url(r"^account/signup/$", 'signup', {"form_class": SignupForm}, name="acct_signup"),
    url(r"^account/associate_accounts/$", 'associate_accounts', name="acct_associate_accounts"),
)

urlpatterns += patterns("",

    url(r"^account/email/$", "pinax.apps.account.views.email", name="acct_email"),
    url(r"^account/login/$", "pinax.apps.account.views.login", name="acct_login"),
    url(r"^account/login/openid/$", "pinax.apps.account.views.login", {"associate_openid": True},
        name="acct_login_openid"),
    url(r"^account/password_change/$", "pinax.apps.account.views.password_change", name="acct_passwd"),
    url(r"^account/password_set/$", "pinax.apps.account.views.password_set", name="acct_passwd_set"),
    url(r"^account/password_delete/$", "pinax.apps.account.views.password_delete", name="acct_passwd_delete"),
    url(r"^account/password_delete/done/$", "django.views.generic.simple.direct_to_template", {
        "template": "account/password_delete_done.html",
    }, name="acct_passwd_delete_done"),
    url(r"^account/timezone/$", "pinax.apps.account.views.timezone_change", name="acct_timezone_change"),

    url(r"^account/language/$", "pinax.apps.account.views.language_change", name="acct_language_change"),
    url(r"^account/logout/$", "django.contrib.auth.views.logout", {"template_name": "account/logout.html"}, name="acct_logout"),

    url(r"^account/confirm_email/(\w+)/$", "emailconfirmation.views.confirm_email", name="acct_confirm_email"),

    # password reset
    url(r"^account/password_reset/$", "pinax.apps.account.views.password_reset", name="acct_passwd_reset"),
    url(r"^account/password_reset/done/$", "pinax.apps.account.views.password_reset_done", name="acct_passwd_reset_done"),
    url(r"^account/password_reset_key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$", "pinax.apps.account.views.password_reset_from_key", name="acct_passwd_reset_key"),
)