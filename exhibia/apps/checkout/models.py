from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_countries import CountryField

class Order(models.Model):
    member = models.ForeignKey("profiles.Member")

    auction = models.OneToOneField('auctions.Auction') #TODO check this
    card = models.ForeignKey("payments.Card") #Replace it with paymentIPN

    shipping_first_name = models.CharField(_("First Name"), max_length=50)
    shipping_last_name = models.CharField(_("Last Name"), max_length=50)
    shipping_address1 = models.CharField(max_length=100)
    shipping_address2 = models.CharField(max_length=100, blank=True)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=30)
    shipping_country = CountryField()
    shipping_zip_code = models.CharField(max_length=10)
    shipping_phone = models.CharField(max_length=30)

    billing_first_name = models.CharField(_("First Name"), max_length=50)
    billing_last_name = models.CharField(_("Last Name"), max_length=50)
    billing_address1 = models.CharField(max_length=100)
    billing_address2 = models.CharField(max_length=100, blank=True)
    billing_city = models.CharField(max_length=100)
    billing_state = models.CharField(max_length=30)
    billing_country = CountryField()
    billing_zip_code = models.CharField(max_length=10)
    billing_phone = models.CharField(max_length=30)

    created = models.DateTimeField(auto_now_add=True)

