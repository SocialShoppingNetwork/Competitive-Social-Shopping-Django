from django import forms
class PledgeForm(forms.Form):
    auction = forms.CharField(max_length=20, widget=forms.HiddenInput)
    amount = forms.FloatField(initial=5.0)
