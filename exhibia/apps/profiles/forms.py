# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext as _
from django.contrib.admin import widgets

from pinax.apps.account.forms import SignupForm

from profiles.models import BillingAddress
from referrals.models import ReferralLink

class BillingForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        exclude = ('user','deleted','shipping')

class DateRangeForm(forms.Form):
    """Form for selection date range """

    start_date = forms.DateField(label=_('Start date'), widget=widgets.AdminDateWidget())
    end_date = forms.DateField(label=_('End date'), widget=widgets.AdminDateWidget())


class ExhibiaSignupForm(SignupForm):
    def save(self, request):
        user = super(ExhibiaSignupForm, self).save(request)
        profile = user.profile
        if request.session.get('ref'):
            profile.referer = request.session.get('ref')
        if request.session.get('referral_link'):
            try:
                profile.referral_url = ReferralLink.objects.get(pk=\
                        int(request.session.get('referral_link')))
            except: pass
        profile.save()
        return user
