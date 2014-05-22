from django import forms


class BuyNowForm(forms.Form):
    SHIPMENT_METHODS = [
        (0, 'Standard Shipping'),
        (1, 'Two-Day Shipping'),
        (2, 'One-Day Shipping'),
    ]

    shipping = forms.ModelChoiceField(queryset=None, empty_label='-------',
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    payment = forms.ModelChoiceField(queryset=None, empty_label='-------',
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    billing = forms.ModelChoiceField(queryset=None, empty_label='-------',
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    method = forms.ChoiceField(choices=SHIPMENT_METHODS, initial=0, widget=forms.RadioSelect())

    def __init__(self, user, **kwargs):
        super(BuyNowForm, self).__init__(**kwargs)
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