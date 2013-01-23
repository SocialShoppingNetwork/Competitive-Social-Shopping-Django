# -*- coding: utf-8 -*-

import hashlib
from datetime import datetime
from urlparse import urlparse

from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.cache import cache
from django.core.urlresolvers import reverse

from django_countries import CountryField
import dbsettings
from social_auth.signals import socialauth_registered
from social_auth.backends import twitter, facebook, google
from referrals.models import ReferralLink

class RewardPoints(dbsettings.Group):
    bid = dbsettings.PositiveIntegerValue(default=1, help_text='points for bid on auction')
    fund = dbsettings.PositiveIntegerValue(default=1, help_text='points for fund auction')
    tweet = dbsettings.PositiveIntegerValue(default=1, help_text='points for tweet')
    like = dbsettings.PositiveIntegerValue(default=1, help_text='points for like in facebook')
    plus = dbsettings.PositiveIntegerValue(default=1, help_text='points for + in g+')
    associate = dbsettings.PositiveIntegerValue(default=1, help_text='points for association with some social network')
    review = dbsettings.PositiveIntegerValue(default=1, help_text='points for review item')
    invite = dbsettings.PositiveIntegerValue(default=1, help_text='points for invitings user')

class RewardBids(dbsettings.Group):
    bid_for_tweet = dbsettings.PositiveIntegerValue(default=1, help_text='bids for tweet')
    bid_for_like = dbsettings.PositiveIntegerValue(default=1, help_text='bids for like in facebook')
    bid_for_plus = dbsettings.PositiveIntegerValue(default=1, help_text='bids for + in g+')
    bid_for_associate = dbsettings.PositiveIntegerValue(default=1, help_text='bids for association with some social network')
    bid_for_review = dbsettings.PositiveIntegerValue(default=1, help_text='bids for review item')
    bid_for_invite = dbsettings.PositiveIntegerValue(default=1, help_text='bids for invitings user')

class Member(models.Model):

    rewards = RewardPoints(verbose_name='Reward points') + RewardBids(verbose_name=u'Reward bids')

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

    points_amount = models.PositiveIntegerField(default=0)
    verified = models.BooleanField(default=False)

    LIKE_SOURCES = {
        'facebook':'like',
        'google-oauth2':'plus'
    }

    def __unicode__(self):
        return unicode(self.user)

    def bid(self, auction):
        auction.bid_by(self)
        self.credits -= 1
        self.points_amount += Member.rewards.bid
        self.save()

    def incr_credits(self, bids, type='P'):
        self.credits += bids
        self.save()

    def buy_package(self, package):
        self.incr_credits(package.total_credits, type='P')
        return self.credits

    def pledge(self, auction, amount):
        auction.pledge(self, amount)
        self.points_amount += Member.rewards.fund
        self.save()

    @property
    def img_url(self):
        if not self.verified:
            return "http://www.gravatar.com/avatar/" + hashlib.md5(self.user.email.lower()).hexdigest()
        avatar_url = cache.get('avatar|%d' % self.pk)
        if avatar_url:
            print 'avatar url is in cache'
            return avatar_url

        backends = self.user.social_auth.all()
        providers = set(i.provider for i in backends)
        print providers
        if 'facebook' in providers:
            url = "http://graph.facebook.com/%s/picture?type=square" % (self.user.username)
        elif 'twitter' in providers:
            # XXX need to set extra params to twitter backend
            # as we have to get avatar via api call
            url = ''
        cache.set('avatar|%d' % self.pk, url , 60*60*24)
        return url


    def invitation_succeed(self):
        self.points_amount += Member.rewards.invite
        self.credits += Member.rewards.bid_for_invite
        self.save()

    def like(self, href, type):
        location = urlparse(href)
        multiply = 1
        if location.path == '/':
            # this is an index page
            multiply = 2
        self.points_amount += getattr(Member.rewards,
                                self.LIKE_SOURCES[type]) * multiply
        self.credits += getattr(Member.rewards,
                                'bid_for_'+self.LIKE_SOURCES[type]) * multiply
        self.save()

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
        ReferralLink.objects.create(user=instance)

@receiver(user_logged_in)
def save_ip(sender, request, user, *args, **kwargs):
    obj, created = IPAddress.objects.get_or_create(user=user,
        IPAddress=request.META.get('X-Real-IP') or request.META.get('REMOTE_ADDR') or '127.0.0.1')
    if not created:
        obj.last_login = datetime.now()
        obj.save()

def user_registered(sender, user, response, details, **kwargs):
    profile = user.get_profile()
    if not profile.verified:
        profile.verified = True
        # this is a place to get an avatar for profile

    profile.points_amount += Member.rewards.associate
    profile.save()

socialauth_registered.connect(user_registered, sender=twitter.TwitterBackend)
socialauth_registered.connect(user_registered, sender=facebook.FacebookBackend)
socialauth_registered.connect(user_registered, sender=google.GoogleBackend)
