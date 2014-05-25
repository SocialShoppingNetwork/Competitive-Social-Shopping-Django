from django import forms
from auctions.models import Auction


class BuyNowForm(forms.Form):

    shipping = forms.ModelChoiceField(queryset=None, empty_label='-------', required=True,
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    payment = forms.ModelChoiceField(queryset=None, empty_label='-------', required=True,
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    billing = forms.ModelChoiceField(queryset=None, empty_label='-------', required=True,
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    method = forms.ModelChoiceField(queryset=None, empty_label=None, widget=forms.RadioSelect(), required=True,)
    auction = forms.ModelChoiceField(queryset=None, widget=forms.HiddenInput(), required=True)

    def __init__(self, user, auction, **kwargs):
        super(BuyNowForm, self).__init__(**kwargs)
        self.user = user
        self.auction = auction
        self.item = auction.item
        billing_addresses = user.billing_addresses.filter(deleted=0)
        if billing_addresses:
            self.fields['billing'].initial = billing_addresses[0]
        self.fields['billing'].queryset = billing_addresses

        shipping_addresses = user.shipping_addresses.filter(deleted=0)
        if shipping_addresses:
            self.fields['shipping'].initial = shipping_addresses[0]
        self.fields['shipping'].queryset = shipping_addresses

        cards = user.card_set.filter(deleted=0)
        if cards:
            self.fields['payment'].initial = cards[0]
        self.fields['payment'].queryset = cards

        self.fields['auction'].queryset = Auction.objects.filter(pk=auction.pk)
        self.fields['auction'].initial = auction

        shipping_fees = auction.item.shipping_fees.all()
        self.fields['method'].queryset = shipping_fees
        if shipping_fees:
            self.fields['method'].initial = shipping_fees[0]


    def method_choices(self):
        """
        Returns myfield's widget's default renderer, which can be used to
            render the choices of a RadioSelect widget.
        """
        field = self['method']
        widget = field.field.widget
        attrs = {}
        auto_id = field.auto_id
        if auto_id and 'id' not in widget.attrs:
            attrs['id'] = auto_id
        name = field.html_name
        return widget.get_renderer(name, field.value(), attrs=attrs)