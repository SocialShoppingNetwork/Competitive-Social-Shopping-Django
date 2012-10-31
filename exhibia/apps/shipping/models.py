from django_countries import CountryField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save

from shipping.constants import SHIPPING_OPTIONS
from shipping.constants import ORDER_WAITING_PAYMENT, ORDER_SHIPPING_FEE_REQUESTED, ORDER_PROCESSING, ORDER_SHIPPED
from shipping.constants import SHIPPING_COMPANIES
from profiles.models import BillingAddress



class ShippingAddress(models.Model):
    user = models.ForeignKey('auth.User', related_name='shipping_adddresses')
    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=30)
    country = CountryField()
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=30)
    deleted = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.user)

class ShippingFee(models.Model):
    item = models.ForeignKey('auctions.AuctionItem')
    country = CountryField()
    shipping = models.CharField(choices=SHIPPING_OPTIONS, max_length=3)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s - %s - %s' % (self.item, self.shipping, self.price)

    @property
    def name(self):
        return dict(SHIPPING_OPTIONS)[self.shipping]

class ShippingRequest(models.Model):
    user = models.ForeignKey("auth.User")
    auction = models.OneToOneField('auctions.Auction') #TODO check this
    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=30)
    country = CountryField()
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=30)
    waiting = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together =('user', 'auction',)

    def __unicode__(self):
        return unicode(self.user)

def create_billing_address(sender, instance, created, raw, **kwargs):
    if instance is None:
        return
    if not created or raw:
        return
    # data = instance.__dict__
    data = {'user':instance.user,
            'first_name':instance.first_name,
            'last_name':instance.last_name,
            'city':instance.city,
            'state':instance.state,
            'country':instance.country,
            'zip_code':instance.zip_code,
            'phone':instance.phone,
            'address1':instance.address1,
            'address2':instance.address1,
            'state':instance.state,
            # 'shipping':instance
    }
    BillingAddress.objects.create(**data)
post_save.connect(create_billing_address, sender=ShippingAddress)

