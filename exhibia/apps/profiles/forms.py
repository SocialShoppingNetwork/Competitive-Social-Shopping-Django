from profiles.models import BillingAddress

from django import forms

class BillingForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        exclude = ('member','deleted','shipping')