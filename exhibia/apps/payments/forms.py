from django import forms
from payments.models import Card
class PledgeForm(forms.Form):
    auction = forms.CharField(max_length=20, widget=forms.HiddenInput)
    amount = forms.FloatField(initial=5.0)

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        exclude = ('member','deleted',)
