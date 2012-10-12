# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext as _
from django.contrib.admin import widgets

from profiles.models import BillingAddress


class BillingForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        exclude = ('member','deleted','shipping')

class DateRangeForm(forms.Form):
    """Form for selection date range """

    start_date = forms.DateField(label=_('Start date'), widget=widgets.AdminDateWidget())
    end_date = forms.DateField(label=_('End date'), widget=widgets.AdminDateWidget())
