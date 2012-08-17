from django_countries import CountryField

from django.db import models
from django.db.models import F
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

from auctions.constants import *
from payments.constants import *

PAYMENT_METHOD = (
    #(PLIMUS, 'Plimus'),
    (DALPAY, 'DalPay'),
    (FACEBOOK_CREDITS, 'Facebook Credits')
)
class PaymentNotification(models.Model):
    token = models.CharField(max_length=255)
    type = models.CharField(max_length=25)
    status = models.CharField(max_length=25)
    item_name = models.CharField(max_length=50, blank=True)
    item_number = models.CharField(max_length=15)
    quantity = models.SmallIntegerField(null=True, blank=True)
    shipping = models.FloatField(null=True, blank=True)
    payer_email = models.CharField(blank=True, max_length=150)
    mc_gross = models.FloatField(null=True, blank=True)
    custom1 = models.CharField(max_length=20, blank=True, null=True) #Token to identify the order
    custom2 = models.CharField(max_length=20, blank=True, null=True) #Token to identify the order
    request_log = models.TextField(blank=True)
    data = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.token

    class Meta:
        ordering = ['-created']

class CreditPackageOrder(models.Model):
    buyer = models.ForeignKey('profiles.Member', related_name='orders', editable=False)
    item = models.ForeignKey('auctions.AuctionItem', blank=True, null=True)
    amount_paid = models.FloatField(default=0)
    pn = models.ForeignKey(PaymentNotification)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return '%s - %s' % (self.buyer, self.paid)

class OnlyFinishedAuctionCanCreateOrder(Exception):
    pass

class AuctionOrderManager(models.Manager):
    def create_order(self, auction, member, method=PLIMUS):
        if auction.status == AUCTION_FINISHED and auction.last_bidder_member == member:
            order =  self.get_query_set().create(auction=auction,
                winner=member,
                status=ORDER_NOT_PAID,
                address=member.address1,
                shipping_fee=auction.item.shipping_fee,
                total=auction.item.price+auction.item.shipping_fee,
            )
            #auction.status = AUCTION_WAITING_PAYMENT
            auction.save()
            return order
        else:
            raise OnlyFinishedAuctionCanCreateOrder

class AuctionOrder(models.Model):
    AUCTION_ORDER_STATUS = (
        (ORDER_NOT_PAID, "Not Paid"),
        (ORDER_PAYMENT_REVIEWING, "Payment Reviewing"),
        (ORDER_PAID, "Paid"),
        (ORDER_CANCELLED, "Cancelled"),
        (ORDER_FINISHED, "Finished"),
        (ORDER_SUSPENDED, "Suspended"),
    )
    auction = models.ForeignKey("auctions.Auction")
    winner = models.ForeignKey("profiles.Member", editable=False)
    amount_paid = models.FloatField(default=0)
    method = models.CharField(max_length=3, choices=PAYMENT_METHOD, default=PLIMUS)
    status = models.CharField(max_length=3, choices=AUCTION_ORDER_STATUS, default=ORDER_NOT_PAID)
    pn = models.ForeignKey(PaymentNotification, blank=True, null=True)
    extra_info = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField(auto_now=True)
    objects = AuctionOrderManager()

    class Meta:
        unique_together = ('auction', 'winner')

    def __unicode__(self):
        return "%s won by %s" % (self.auction, self.winner)

    class Meta:
        ordering = ["-id"]

class Card(models.Model):
    member = models.ForeignKey("profiles.Member")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    number = models.CharField(max_length=30)
    expiration_month = models.PositiveSmallIntegerField()
    expiration_year = models.PositiveSmallIntegerField()

    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return "%s" % (self.number)
