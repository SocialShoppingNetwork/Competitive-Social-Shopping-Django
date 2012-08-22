from django_countries import CountryField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save

from shipping.constants import SHIPPING_STANDARD, SHIPPING_EXPEDITED, SHIPPING_SAME_DAY, SHIPPING_INTERNATIONAL
from shipping.constants import SHIPPING_COMPANY_FEDEX, SHIPPING_COMPANY_USPS, SHIPPING_COMPANY_UPS, SHIPPING_COMPANY_DHL
from shipping.constants import ORDER_WAITING_PAYMENT, ORDER_SHIPPING_FEE_REQUESTED, ORDER_PROCESSING_ORDER, ORDER_SHIPPED
from profiles.models import BillingAddress

SHIPPING_OPTIONS = (
    (SHIPPING_STANDARD, 'Shipping Standard'),
    (SHIPPING_EXPEDITED, 'Shipping Expedited'),
    (SHIPPING_SAME_DAY, 'Shipping Same day'),
    (SHIPPING_INTERNATIONAL, 'International Shipping')
)

class ShippingAddress(models.Model):
    member = models.ForeignKey('profiles.Member')
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
        return str(self.member)

class ShippingFee(models.Model):
    item = models.ForeignKey('auctions.AuctionItem')
    country = CountryField()
    shipping = models.CharField(choices=SHIPPING_OPTIONS, max_length=3)
    price = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s - %s - %s' % (self.item, self.shipping, self.price)
    @property
    def name(self):
        d = dict(SHIPPING_OPTIONS)
        return d[self.shipping]

SHIPPING_COMPANIES = (
    (SHIPPING_COMPANY_FEDEX, 'FEDEX'),
    (SHIPPING_COMPANY_USPS, 'USPS'),
    (SHIPPING_COMPANY_UPS, 'UPS'),
    (SHIPPING_COMPANY_DHL, 'DHL')
)

ORDER_STATUS = (
    (ORDER_WAITING_PAYMENT, "Waiting Payment"),
    (ORDER_SHIPPING_FEE_REQUESTED, "Shipping fee Requested"),
    (ORDER_PROCESSING_ORDER, "Processing order"), #PAID
    (ORDER_SHIPPED, "Shipped"),
)

class ShippingRequest(models.Model):
    member = models.ForeignKey("profiles.Member")
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
        unique_together =('member', 'auction',)
    def __unicode__(self):
        return str(self.member)

def create_billing_address(sender, instance, created, raw, **kwargs):
    if instance is None:
        return
    if not created:
        return
    data = instance.__dict__
    data = {'member':instance.member,
            'first_name':instance.first_name,
            'last_name':instance.last_name,
            'city':instance.city,
            'state':instance.state,
            'country':instance.country,
            'zip_code':instance.zip_code,
            'phone':instance.phone,
            'shipping':instance
    }
    BillingAddress.objects.create(**data)
post_save.connect(create_billing_address, sender=ShippingAddress)

