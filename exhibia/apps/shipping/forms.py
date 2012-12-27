from shipping.models import ShippingAddress

from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import HiddenInput
from django.conf import settings
from datetime import datetime
from django.contrib.localflavor.ca import forms as forms_ca
from django.contrib.localflavor.us import forms as forms_us
from django.contrib.localflavor.uk import forms as forms_uk

class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        exclude = ('user','deleted', )

class MemberInfoFormUS(forms.ModelForm):

    zip_code = forms_us.USZipCodeField(help_text='format XXXXX or XXXXX-XXXX')
    state = forms_us.USStateField(widget=forms_us.USStateSelect())
    phone = forms_us.USPhoneNumberField(help_text='format XXX-XXX-XXXX')

    class Meta:
        model = ShippingAddress
        exclude = ('user','deleted', )


def get_shipping_form(request=None):
    if request is None:
        return MemberInfoFormUS
