# -*- coding: utf-8 -*-

import settings

from time import time
from random import randint
from datetime import datetime

from django.db import models
from django.db.models import F
from django.db.models import Avg, Max, Min, Count
from django.core.validators import RegexValidator
from django_countries import CountryField

from auctions.exceptions import AlreadyHighestBid, AuctionExpired, AuctionIsNotReadyYet, NotEnoughCredits, AuctionLocked

from utils import full_url
from auctions.constants import *
from storages.backends.mosso import cloudfiles_upload_to

AUCTION_WAITING = 'w'
AUCTION_PROCESSING = 'p'
AUCTION_PAUSE = 's'
AUCTION_JUST_ENDED = 'e'
AUCTION_FINISHED = 'f'
AUCTION_WAITING_PAYMENT = 'm'
AUCTION_PAID = 'd'
AUCTION_COMPLETED = 'c'

AUCTION_STATUS = (
    (AUCTION_WAITING_PLEDGE, "Waiting pledge"),
    (TRANSITION_PHASE_1, "Transition phase 1"),
    (AUCTION_SHOWCASE, "Showcase"),
    (AUCTION_PAUSE, "Pause"),
    (AUCTION_JUST_ENDED, "Just Ended"),
    (TRANSITION_PHASE_2, "Transition phase 2"),
    (AUCTION_FINISHED, "Finished"),
    (AUCTION_FINISHED_NO_PLEDGED, "Finished without pledged the price"),
    (AUCTION_WAITING_PAYMENT, "Waiting Payment"), #NEW
    (AUCTION_PAID, "Paid"),
    (AUCTION_COMPLETED, "Completed"),
)


# ORDER_WAITING_PAYMENT = 'wp'
# ORDER_SHIPPING_FEE_REQUESTED = 'rf'
# ORDER_PROCESSING_ORDER = 'rf'
# ORDER_DELIVERED = 'dl'
# ORDER_WAITING_TESTIMONIAL = 'wt'

# ORDER_STATUS = (
#     (ORDER_WAITING_PAYMENT, "Waiting Payment"),
#     (ORDER_SHIPPING_FEE_REQUESTED, "Shipping fee Requested"),
#     (ORDER_PROCESSING_ORDER, "Processing order"), #PAID
#     (ORDER_DELIVERED, "Delivered"),
#     (ORDER_WAITING_TESTIMONIAL, "Waiting Testimonial"),
# )

BID_TYPE_CHOICES = (
    ("n", "Normal"),
    ("m", "bid-o-matic"),
)


class AuctionManager(models.Manager):
    def waiting_pledge(self):
        return self.get_query_set().filter(status=AUCTION_WAITING_PLEDGE)

    def transition_phase_1(self):
        return self.get_query_set().filter(status=TRANSITION_PHASE_1)

    def transition_phase_2(self):
        return self.get_query_set().filter(status=TRANSITION_PHASE_2)

    def time_over(self):
        return self.waiting_pledge().filter(deadline_time__lte=time())

    def showcase(self):
        return self.get_query_set().filter(status=AUCTION_SHOWCASE)

    def about_to_start(self):
        pass

    def public(self):
        return self.get_query_set().filter(
            status__in=[AUCTION_SHOWCASE, AUCTION_PAUSE, AUCTION_JUST_ENDED, AUCTION_WAITING_PLEDGE])

    def live(self):
        return self.get_query_set().filter(status__in=[AUCTION_SHOWCASE, AUCTION_PAUSE, TRANSITION_PHASE_2])
        #return self.get_query_set().filter(status__in=['w', 'p', 's', 'e'])

    #def live(self):
    #    return self.get_query_set().filter(status__in=['w', 'p', 's', 'e'])

    #def running(self):
    #    return self.filter(status='p')

    def paused(self):
        return self.get_query_set().filter(status=AUCTION_PROCESSING)

    #def waiting(self):
    #    return self.get_query_set().filter(status='w')

    def finished(self):
        return self.get_query_set().filter(status=AUCTION_FINISHED)

    def just_ended(self):
        return self.get_query_set().filter(status=AUCTION_JUST_ENDED)

    def expired(self):
        return self.just_ended().filter(ended_unixtime__lte=time() - settings.MAX_TIME_HOMEPAGE)

    def about_end(self):
        return self.running().filter(last_unixtime__lte=time() - F('bidding_time'))

    def finish_expired(self):
        self.expired().update(status=AUCTION_FINISHED)

    def create_from_item(self, item):
        auction = Auction.objects.create(item=item,
                                         bidding_time=item.bidding_time,
                                         deadline_time=time() + item.pledge_time,
                                         status=AUCTION_WAITING_PLEDGE,
        )
        if item.amount is not None:
            item.amount -= 1
        item.save()
        return auction

    def create_giveaway_from_item(self, item):
        auction = Auction.objects.create(item=item,
                                         bidding_time=item.bidding_time,
                                         deadline_time=time() + item.pledge_time,
                                         status=AUCTION_SHOWCASE,
                                         amount_pleged=item.price,
        )
        if item.amount is not None:
            item.amount -= 1
        item.save()
        return auction


class AuctionItemManager(models.Manager):
    def kick_off(self):
        items = self.get_query_set().exclude(code__in=Auction.objects.waiting_pledge().values_list('item', flat=True),
                                             amount__gt=0)
        if items.count() > 0:
            i = randint(0, items.count() - 1)
            item = items[i]
            return item
            #return Auction.objects.create_from_item(item)

    def get_giveaway_item(self):
        # get items which aren't in showcase list, as well as not in waiting pledge
        print Auction.objects.showcase().values_list('item', flat=True)
        items = self.get_query_set() \
            .filter(giveaway=True) \
            .exclude(amount=0) \
            .exclude(code__in=Auction.objects.showcase().values_list('item', flat=True))
        # .exclude(code__in=Auction.objects.waiting_pledge().values_list('item', flat=True))

        if items.count() > 0:
            i = randint(0, items.count() - 1)
            item = items[i]
            return item


class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, unique=True)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Category'
        verbose_name_plural = u'Categories'


from tinymce import models as tinymce_models


class AuctionItem(models.Model):
    code = models.CharField(max_length=15,
                            primary_key=True,
                            db_index=True,
                            validators=[RegexValidator('^[a-zA-Z0-9-]+$')],
                            help_text="""This field is used to identify p, make sure its value is UNIQUE,\
                            it is NOT allowed to modify after the first time you add it.\
                            Only letters, numbers or hyphens are valid""")

    name = models.CharField(max_length=150)
    slug_name = models.CharField(max_length=200, unique=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    amount = models.SmallIntegerField(null=True, blank=True)
    brand = models.ForeignKey(Brand, blank=True, null=True)
    categories = models.ManyToManyField(Category, blank=True, null=True)

    pledge_time = models.PositiveIntegerField(default=settings.PLEDGE_TIME)

    showcase_time = models.PositiveIntegerField(default=settings.SHOWCASE_TIME)

    bidding_time = models.SmallIntegerField(default=120)
    shipping_fee = models.DecimalField(max_digits=7, decimal_places=2)
    description = tinymce_models.HTMLField(default='', blank=True)

    notes = models.TextField(default='', blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    objects = AuctionItemManager()
    image = models.OneToOneField('auctions.AuctionItemImages', blank=True, null=True)

    giveaway = models.BooleanField()

    # lock item after X bids
    lock_after = models.PositiveIntegerField(blank=True, null=True, verbose_name='Lock item after how many bids?')
    # item is only for new users (which have never been winners)
    newbie = models.BooleanField()

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('auction_item', [self.slug_name])

    def get_full_url(self):
        return full_url(self.get_absolute_url())

    def get_full_image_url(self):
        image = self.default_image
        if image:
            return image.get_full_url()
        return ''

    @property
    def default_image(self):
        return self.image
        #try:
        #    image = self.images.filter(is_default=True)[0]
        #    return image
        #except:
        #    return None

    def categories_inline(self):
        return ', '.join([i.name for i in self.categories.all()])

    categories_inline.short_description = "categories"


class Auction(models.Model):
    item = models.ForeignKey(AuctionItem, related_name='auctions', db_index=True)
    #status = models.CharField(max_length=1, default=AUCTION_WAITING_PLEDGE, choices=AUCTION_STATUS, db_index=True)
    status = models.CharField(max_length=2, default=AUCTION_WAITING_PLEDGE, choices=AUCTION_STATUS, db_index=True)

    #order_status = models.CharField(max_length=2, blank=True, null=True, choices=ORDER_STATUS, db_index=True)
    #waiting payment, processign order, upload testimonial

    amount_pleged = models.PositiveIntegerField(default=0)
    backers = models.PositiveIntegerField(default=0)
    current_offer = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    pledge_time = models.PositiveIntegerField(default=43200)

    deadline_time = models.FloatField(db_index=True)
    bidding_time = models.PositiveSmallIntegerField()
    last_bidder = models.CharField(max_length=30, default='', db_index=True, blank=True)
    last_bidder_member = models.ForeignKey('auth.User', blank=True, null=True, related_name='items_won')  #winner

    last_bid_type = models.CharField(max_length=1, default='n', choices=BID_TYPE_CHOICES, blank=True,
                                     null=True) #Todo remove this field
    last_unixtime = models.FloatField(null=True, blank=True, db_index=True)
    ended_unixtime = models.FloatField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    objects = AuctionManager()

    in_queue = models.BooleanField()

    locked = models.BooleanField()

    def __unicode__(self):
        return self.item.name

    @models.permalink
    def get_absolute_url(self):
        return 'auction_item', (), {'slug': self.item.slug_name}

    @property
    def time_to_go(self):
        if self.status != AUCTION_WAITING_PLEDGE:
            return -1
        return self.deadline_time - time()

    def pledge(self, member, amount):
        self.amount_pleged += amount
        if not AuctionPlegde.objects.filter(auction=self, member=member).exists():
            self.backers += 1
        AuctionPlegde.objects.create(auction=self, member=member, amount=amount)
        self.save()

    @property
    def is_processing(self):
        return self.status == AUCTION_SHOWCASE

    @property
    def is_waiting_pledge(self):
        return self.status == AUCTION_WAITING_PLEDGE

    @property
    def is_paused(self):
        return self.status == AUCTION_PAUSE

    @property
    def is_running(self):
        return self.is_processing or self.is_paused

    @property
    def funded(self):
        """returns the percent funded"""
        return float(self.amount_pleged * 100 / self.item.price)

    @property
    def time_left(self):
        if not self.last_unixtime:
            return self.bidding_time
        return int(self.last_unixtime + self.bidding_time - time())
        #t = self.last_unixtime + self.bidding_time - time()
        return int(round(t + 0.49))

    # @property
    # def time_left_for_bidding_start(self):
    #     return 180
    @property
    def bidding_start_at(self):
        return datetime.fromtimestamp(int(settings.TRANSITION_PHASE_1_TIME + self.last_unixtime))

    def end_dt(self):
        return datetime.fromtimestamp(int(self.last_unixtime))

    @property
    def is_ended(self):
        return self.ended_unixtime != None

    def end(self):
        self.status = AUCTION_JUST_ENDED
        # self.ended_unixtime = time()
        # if self.last_bidder_member:
        #     self.order_status = ORDER_WAITING_PAYMENT
        self.save()

    def transition_phase_2(self):
        self.status = TRANSITION_PHASE_2
        self.ended_unixtime = time()
        if self.last_bidder_member:
            self.order_status = ORDER_WAITING_PAYMENT
        self.save()

    def pause(self):
        self.status = AUCTION_PAUSE
        self.save()

    def resume(self):
        if self.current_offer == 0.0:
            self.status = AUCTION_WAITING_PLEDGE
        else:
            self.status = AUCTION_SHOWCASE
        self.save()

    def bid_by(self, bidder):
        if self.status in ['f', 'm', 'd', 'c', 'e']:
            raise AuctionExpired

        username = bidder.user.username
        if bidder.credits <= 0:
            raise NotEnoughCredits

        if self.last_bidder == username:
            #TODO check this only raise without conditions, no win require, no conditions
            raise AlreadyHighestBid

        # the auction is locked
        if self.locked:
            #check user
            if not AuctionBid.objects.filter(auction=self, bidder=bidder).exists():
                raise AuctionLocked

        #if self.status == "w":
        #    raise AuctionIsNotReadyYet

        # Paused Auction Will still accept bid
        #elif self.status == "s":
        #    raise AuctionPaused

        bid_type = 'n'
        price = self.current_offer + settings.PRICE_INTERVAL
        unixtime = time()
        if self.status == 'w':
            self.status = 'p'

        AuctionBid.objects.create(auction=self, bidder=bidder, unixtime=unixtime, price=price)
        self.last_bidder = username
        self.last_bidder_member = bidder.user
        self.last_bid_type = bid_type
        self.last_unixtime = time()
        self.current_offer = price

        #lock item after "item.lock_after" bids

        if self.item.lock_after == self.bids.count():
            self.locked = True

        self.save()

    @property
    def backers_history(self):
        from profiles.models import Member

        return Member.objects.filter(auctionplegde__auction=self).distinct().annotate(
            pledge_date=Max('auctionplegde__created'))

    @property
    def bidding_history(self):
        return AuctionBid.objects.filter(auction=self).order_by('-created')

    def total_price(self):
        return self.current_offer + self.item.shipping_fee


class AuctionBid(models.Model):
    auction = models.ForeignKey(Auction, related_name='bids')
    bidder = models.ForeignKey('profiles.Member')
    price = models.DecimalField(max_digits=7, decimal_places=2)
    unixtime = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s : %s ' % (self.auction, self.bidder)


class AuctionItemImages(models.Model):
    item = models.ForeignKey(AuctionItem, related_name="images")
    img = models.ImageField(help_text="default image 120px height 200px width recommended",
                            upload_to=cloudfiles_upload_to)
    is_default = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.img)

    def get_full_url(self):
        return full_url(self.img.url)

    def save(self, *args, **kwargs):
        super(AuctionItemImages, self).save(*args, **kwargs)
        if self.is_default:
            self.item.image = self
            self.item.save()

    class Meta:
        verbose_name = u'auction item image'
        verbose_name_plural = u'auction item images'


class AuctionPlegde(models.Model):
    auction = models.ForeignKey(Auction)
    member = models.ForeignKey('profiles.Member')
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s %s' % (self.auction, self.member)


