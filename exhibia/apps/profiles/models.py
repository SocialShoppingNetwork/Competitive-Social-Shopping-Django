# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from django_countries import CountryField

class Member(models.Model):

    user = models.OneToOneField(User, verbose_name=_("user"), related_name='profile')
    about = models.TextField(_("about"), null=True, blank=True)
    location = models.CharField(_("location"), max_length=40, null=True, blank=True)
    website = models.URLField(_("website"), null=True, blank=True, verify_exists=False)
    credits = models.PositiveIntegerField(default=3)

    address1 = models.CharField(max_length=100, blank=True)
    address2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    state = models.CharField(max_length=30, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True,
                             help_text="for example: 1980-7-9")
    referer = models.CharField(max_length=100, blank=True, null=True)
    referral_url = models.ForeignKey('referrals.ReferralLink', blank=True,
                 null=True, related_name='invited_users')
    #chat
    is_banned = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.user)

    def bid(self, auction):
        auction.bid_by(self)
        self.credits -= 1
        self.save()

    def incr_credits(self, bids, type='P'):
        self.credits += bids
        self.save()

    def buy_package(self, package):
        self.incr_credits(package.total_credits, type='P')
        return self.credits

    def pledge(self, auction, amount):
        auction.pledge(self, amount)

    @property
    def img_url(self):
        return "http://graph.facebook.com/%s/picture?type=square" % (self.user.username)
    """
    def auctionorders_unpaid(self):
        return AuctionOrder.objects.filter(auction__status="m", winner=self)

    def auctionorders_paid(self):
        return AuctionOrder.objects.filter(auction__status="d", winner=self)

    def auctionorders_history(self):
        return AuctionOrder.objects.filter(auction__status="c", winner=self)"""


"""
def create_shipping_profile(sender, instance=None, **kwargs):
    if instance is None:
        return
    profile, created = ShippingProfile.objects.get_or_create(member=instance,
                                                             defaults={'first_name':instance.user.first_name,
                                                                       'last_name':instance.user.last_name,
                                                                       'address1':instance.address1,
                                                                       'address2':instance.address2,
                                                                       'city':instance.city,
                                                                       'zip_code':instance.zip_code,
                                                                       'state':instance.state,
                                                                       'phone':instance.phone})
post_save.connect(create_shipping_profile, sender=Member)
"""

class BillingAddress(models.Model):

    user = models.ForeignKey(User, related_name='billing_addresses')
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


class IPAddress(models.Model):
    user = models.ForeignKey(User, related_name='ip_addresses')
    IPAddress = models.IPAddressField()
    last_login = models.DateField(default=datetime.now)

    def __unicode__(self):
        return ''

    class Meta:
        unique_together = ('user', 'IPAddress')
        ordering = ('-last_login', )
        verbose_name_plural = 'IP addresses'

class BannedIPAddress(models.Model):
    IPAddress = models.IPAddressField()
    created_at = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.IPAddress)

    class Meta:
        app_label = "auth"
        db_table = "profiles_bannedipaddress"
        verbose_name_plural = 'Banned IP addresses'



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, raw,**kwargs):
    if created and not raw:
        Member.objects.create(user=instance)

@receiver(user_logged_in)
def save_ip(sender, request, user, *args, **kwargs):
    obj, created = IPAddress.objects.get_or_create(user=user,
        IPAddress=request.META.get('X-Real-IP') or request.META.get('REMOTE_ADDR') or '127.0.0.1')
    if not created:
        obj.last_login = datetime.now()
        obj.save()
