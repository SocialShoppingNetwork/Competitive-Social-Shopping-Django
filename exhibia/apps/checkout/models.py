from auctions.constants import ORDER_PAID
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_countries import CountryField

from shipping.constants import ORDER_WAITING_PAYMENT, ORDER_SHIPPING_FEE_REQUESTED, ORDER_PROCESSING, ORDER_SHIPPED, SHIPPING_COMPANIES
from shipping.constants import SHIPPING_COMPANIES_DICT

ORDER_STATUS = (
    (ORDER_PROCESSING, "Processing order"),
    (ORDER_SHIPPED, "Shipped"),
    (ORDER_PAID, "Paid"),
)


class Order(models.Model):
    user = models.ForeignKey("auth.User", related_name="orders")
    auction = models.ForeignKey('auctions.Auction')  # TODO check this
    card = models.ForeignKey("payments.Card")  # Replace it with paymentIPN
    tracking_number = models.CharField(max_length=25, blank=True, null=True)
    shipping_company = models.CharField(max_length=5, choices=SHIPPING_COMPANIES, blank=True, default=True)
    shipping_fee = models.ForeignKey("shipping.ShippingFee")
    status = models.CharField(max_length=2, choices=ORDER_STATUS, default=ORDER_PROCESSING)
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

    class Meta:
        unique_together = ('user', 'auction',)

    @property
    def shipping_company_name(self):
        return SHIPPING_COMPANIES_DICT.get(self.shipping_company)

    def is_shipped(self):
        return self.status == ORDER_SHIPPED

    def is_processing(self):
        return self.status == ORDER_PROCESSING

    def __unicode__(self):
        return '%s | %s - %s' % (self.auction.item.name, self.user, self.created)

