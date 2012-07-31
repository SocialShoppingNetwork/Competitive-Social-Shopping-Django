from random import randint
import logging

from django.db import models
from django.db.models.signals import post_save

from auctions.models import AuctionItem
from auctions.exceptions import AuctionIsNotReadyYet, AuctionExpired, AlreadyHighestBid

from profiles.models import Bot
from auctions.models import Auction

"""
class AuctionMaticBid(models.Model):
    auction = models.OneToOneField("auctions.Auction", related_name="maticbid", unique=True)
    #max_bids = models.SmallIntegerField(default=500)
    bids_left = models.SmallIntegerField(default=500)
    lastbid_unixtime = models.FloatField(blank=True, null=True)
    win = models.BooleanField(default=False)
    bots = models.ManyToManyField("profiles.Bot", blank=True, null=True)
    def __unicode__(self):
        return self.auction.item.name

    def bid(self, auction):
        try:
            if self.bots.count() >1:
                bots = self.bots.exclude(username=auction.last_bidder)
                #bots = self.bots.exclude(username__in=[auction.latest_bidder])
            else: #WIN
                bots = self.bots.all()
            if not bots.exists():
                logging.critical("There aren't bot to bid - Auction %s" % self.auction.pk)
                if Bot.objects.exists():
                    bots_count = Bot.objects.count()
                    index = randint(0, bots_count-1)
                    bot = Bot.objects.all()[index]
                else:
                    logging.critical("Bot table is empty")
                    raise ThereAreNoBotAvailable
            else:
                num_bots = bots.count()
                bot = bots[randint(0, num_bots-1)]
            if bot:
                result = bot.bid(auction)
                self.bids_left -= 1
                self.lastbid_unixtime = auction.last_unixtime
                self.save()
        except AlreadyHighestBid, e:
            pass
        except AuctionIsNotReadyYet, e:
            pass
        except Exception, e:
            print e

    @property
    def users_bid(self):
        return self.auction.auctionbid_set.count()

    def set_bots(self, num_bots):
        if self.win:
            num_bots = 1
        if num_bots >= self.bots.count():
            bots = Bot.objects.available()[:num_bots]
        else:
            bots = list(self.bots.all().order_by("?")[:num_bots])
        self.bots = bots
        self.save()
        if not self.bots.exists():
            logging.critical("Bots count: %s" % num_bots)

class MaticBid(models.Model):
    item = models.OneToOneField('auctions.AuctionItem', related_name="maticbid", unique=True)
    max_bids = models.SmallIntegerField()

    def __unicode__(self):
        return self.item.name

    def create_auction_maticbid(self, auction):
        bots = Bot.objects.exclude(id__in=list(Auction.objects.live().exclude(maticbid__bots=None).values_list('maticbid__bots',flat=True))).order_by("?")[:20]


        matic_bid = AuctionMaticBid.objects.create(auction=auction,
                                                   #max_bids=self.max_bids,
                                                   bids_left=self.max_bids)
        matic_bid.bots = list(bots)
        matic_bid.save()
        return matic_bid

def create_bidomatic_item(sender, instance, created, **kargs):
    if created:
        try:
            MaticBid.objects.get(item=instance)
        except MaticBid.DoesNotExist:
            matic = MaticBid(item=instance, max_bids=500)
            matic.save()
post_save.connect(create_bidomatic_item, AuctionItem)

"""