from django.conf import settings
from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from pinax.apps.account.utils import get_default_redirect, user_display
from pinax.apps.account.views import group_and_bridge, group_context

from social_login.forms import SignupForm
from social_auth import __version__ as version
from social_auth.backends import UID_CONFIRMED, UID_USERNAME, BACKENDS, OpenIdAuth, BaseOAuth, BaseOAuth2
from referrals.models import ReferralLink
from annoying.decorators import render_to


@render_to('login/callback.html')
def callback(request):
    user_info = request.session.pop(settings.SOCIAL_AUTH_INFO_KEY, None)
    return {'user_info': user_info,
            'uid_confirmed_name': UID_CONFIRMED}


@render_to('login/error.html')
def error(request):
    error_msg = request.session.pop(settings.SOCIAL_AUTH_ERROR_KEY, None)
    return {'error_msg': error_msg}



def signup(request, **kwargs):

    form_class = kwargs.pop("form_class", SignupForm)
    template_name = kwargs.pop("template_name", "account/signup.html")
    redirect_field_name = kwargs.pop("redirect_field_name", "next")
    success_url = kwargs.pop("success_url", None)

    group, bridge = group_and_bridge(kwargs)
    ctx = group_context(group, bridge)

    if success_url is None:
        if hasattr(settings, "SIGNUP_REDIRECT_URLNAME"):
            fallback_url = reverse(settings.SIGNUP_REDIRECT_URLNAME)
        else:
            if hasattr(settings, "LOGIN_REDIRECT_URLNAME"):
                fallback_url = reverse(settings.LOGIN_REDIRECT_URLNAME)
            else:
                fallback_url = settings.LOGIN_REDIRECT_URL
        success_url = get_default_redirect(request, fallback_url, redirect_field_name)
    uid = ''
    if request.method == "POST":
        form = form_class(request.POST, group=group)
        backend = request.POST.get('backend')
        uid = request.POST.get(UID_CONFIRMED)
        if request.POST.get('new'):
            form.del_errors()
        else:
            if backend:
                is_valid = form.is_valid_for_backend()
                if is_valid:
                    username = form.cleaned_data['username']
                    request.session[UID_CONFIRMED] = request.POST.get(UID_CONFIRMED)
                    request.session[UID_USERNAME] = username
                    url = '%s?%s=%s' % (reverse('socialauth_begin', kwargs=dict(backend=backend)),
                                        REDIRECT_FIELD_NAME, success_url)
                    return HttpResponseRedirect(url)
            else:
                if form.is_valid():
                    user = form.save(request=request)
                    profile = user.profile
                    if request.session.get('ref'):
                        profile.referer = request.session.get('ref')
                    if request.session.get('referral_link'):
                        try:
                            profile.referral_url = ReferralLink.objects.get(pk=\
                                    int(request.session.get('referral_link')))
                        except: pass
                    profile.save()
                    if settings.ACCOUNT_EMAIL_VERIFICATION:
                        ctx.update({
                            "email": form.cleaned_data["email"],
                            "success_url": success_url,
                        })
                        ctx = RequestContext(request, ctx)
                        return render_to_response("account/verification_sent.html", ctx)
                    else:
                        form.login(request, user)
                        messages.add_message(request, messages.SUCCESS,
                            ugettext("Successfully logged in as %(user)s.") % {
                                "user": user_display(user)
                            }
                        )
                        return HttpResponseRedirect(success_url)
    else:
        form = form_class(group=group)

    ctx.update({
        "form": form,
        "redirect_field_name": redirect_field_name,
        "redirect_field_value": request.REQUEST.get(redirect_field_name),
        'uid_confirmed_name': UID_CONFIRMED,
        'uid': uid
    })

    return render_to_response(template_name, RequestContext(request, ctx))


def grouped_backends():
    """Group backends by type"""
    backends = {'oauth': [],
                'oauth2': [],
                'openid': []}

    for name, backend in BACKENDS.iteritems():
        if issubclass(backend, BaseOAuth2):
            key = 'oauth2'
        elif issubclass(backend, BaseOAuth):
            key = 'oauth'
        elif issubclass(backend, OpenIdAuth):
            key = 'openid'
        else:
            print name, backend
        backends[key].append((name, backend))
    return backends


@login_required
@render_to('account/associate_accounts.html')
def associate_accounts(request):
    return {'accounts': request.user.social_auth.all(),
           'version': version,
           'error': request.session.pop(settings.SOCIAL_AUTH_ERROR_KEY, None),
           'disconnect_error': request.session.pop(settings.SOCIAL_DISCONNECT_AUTH_ERROR_KEY, None),
           'last_login': request.session.get('social_auth_last_login_backend'),
           'backends': grouped_backends()}


