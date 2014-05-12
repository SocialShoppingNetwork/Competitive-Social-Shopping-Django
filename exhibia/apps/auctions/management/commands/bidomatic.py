# -*- coding: utf-8 -*-

# from random import randint
from time import sleep, time
import threading
import json
# import cjson

from django.conf import settings
from django.db.models import F
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
# from django.core.cache import cache

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from auctions.models import Auction, AuctionItem
from auctions.constants import *
from profiles.models import Member
import sys
from apps.auctions import constants


def to_json(auction):
    result = {"id": auction.id,
            "status": auction.status,
            "last_bidder": auction.last_bidder,
            "time_left": auction.time_left,
            "current_price": auction.current_offer,
            "bidding_time": auction.bidding_time}
    if auction.last_bidder_member:
        result["last_bidder_img"] = auction.last_bidder_member.img_url
    return result


def auctions_to_json(auctions):
    result = {}
    for a in auctions:
        result['a_%s' % a.id] =  to_json(a)
    return result


# class UpdateCache(threading.Thread):
#     def __init__(self):
#         print settings.CACHES
#         threading.Thread.__init__(self)
#         self.kill_received = False

#     def run(self):
#         while not self.kill_received:
#             auctions = Auction.objects.live().order_by('id').select_related('item', 'item__image')
#             cache.set('auctions', auctions)
#             auctions = auctions_to_json(auctions)
#             d = {}
#             for k,v in auctions.items():
#                 cache.set(k, cjson.encode({k:v}), 30)
#             auctions_json = cjson.encode(auctions)
#             print 'updating cache'
#             cache.set('auctions_json', auctions_json, 30)

#             cache.get('auctions_json')
#             sleep(0.5)


class KillReceived(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(KillReceived, self).__init__(*args, **kwargs)
        self.kill_received = False


class KickOff(KillReceived):

    def run(self):
        ### THIS NOT RUNNING FOR NOW
        while not self.kill_received:

            # here we must
            ## for bidded I thinhk
            # MIN_ACTIVE_AUCTIONS

            # waiting_pledge() - открытые для funda
            # show_case - открытые для bida (и уже забиденные кем-то)
            flush_transaction()

            # # adds giveaway item if active auctions less than in settings
            # if Auction.objects.showcase().count() < settings.MIN_ACTIVE_AUCTIONS:
            #     '--->>> not enought active actions!'
            #     item = AuctionItem.objects.get_giveaway_item()
            #     auction = Auction.objects.create_giveaway_from_item(item)
            #     print '--->>> add giveaway auction \n'



            # if Auction.objects.waiting_pledge().count() < settings.MAX_AUCTIONS:
            #     item = AuctionItem.objects.kick_off()
            #     auction = Auction.objects.create_from_item(item)
            #     #item.maticbid.create_auction_maticbid(auction)
            #     # print 'kickoff auction : %s' % auction
            Auction.objects.finish_expired()
            sleep(5)


class Dispatcher(KillReceived):

    def run(self):
        while not self.kill_received:

            flush_transaction()
            now = time()

            ## checking for auctions in queue, if there are empty slots, make them active
            if Auction.objects.waiting_pledge().filter(in_queue=True):
                available_slots = settings.MAX_AUCTIONS - Auction.objects.showcase().count()
                if available_slots > 0:
                    print '--->>> move from queue \n'
                    Auction.objects.waiting_pledge()[:available_slots].update(in_queue=False, status=constants.AUCTION_SHOWCASE)

            if Auction.objects.showcase().count() < settings.MAX_AUCTIONS:
                item = AuctionItem.objects.get_giveaway_item()
                if item:
                    Auction.objects.create_giveaway_from_item(item)
                    print '--->>> add giveaway auction \n'

            ## adds giveaway item if active auctions less than in settings
            if Auction.objects.showcase().count() < settings.MIN_ACTIVE_AUCTIONS:
                item = AuctionItem.objects.get_giveaway_item()
                if item:
                    Auction.objects.create_giveaway_from_item(item)
                    print '--->>> add giveaway auction \n'

            ## changes items, wich were fully funded, to active auctions
            auctions_time_over = Auction.objects.time_over()



            ### NEW
            # if auctions_time_over:
            #     auctions_funded = auctions_time_over.filter(amount_pleged__gte=F('item__price'))
            #     print '>>>>>>>>>>>>>>>>>'
            #     print auctions_funded
            #     print '<<<<<<<<<<<<<<<<<'
            #     if auctions_funded:
            #         showcase_auctions_count = Auction.objects.showcase().count()
            #         available_count = settings.MAX_AUCTIONS - showcase_auctions_count
            #         auctions_funded[:available_count].update(status=AUCTION_SHOWCASE)
            #         auctions_funded[available_count:].update(in_queue=True)
            ### NEW

            ### OLD
            ## changes items, wich were fully funded, to active auctions
            if auctions_time_over:
                auctions_funded = auctions_time_over.filter(amount_pleged__gte=F('item__price'))
                auctions_funded.update(status=AUCTION_SHOWCASE)
            ### OLD

                #auctions_not_funded = Auction.objects.filter(amount_pleged__lt=F('item__price'))
                #auctions_not_funded.update(status=AUCTION_FINISHED_NO_PLEDGED)

            # if Auction.objects.waiting_pledge().count() < settings.MAX_AUCTIONS:
            #     item = AuctionItem.objects.kick_off()
            #     if item:
            #         auction = Auction.objects.create_from_item(item)
            #         print 'kickoff auction : %s' % auction

            Auction.objects.finish_expired()
            sleep(5)


@transaction.commit_manually
def flush_transaction():
    """
    Flush the current transaction so we don't read stale data
    """
    transaction.commit()


class Bidomatic(KillReceived):

    def run(self):
        while not self.kill_received:
            flush_transaction()

            for auction in Auction.objects.showcase():
                t = auction.time_left
                """
                bidomatic = auction.maticbid
                if t > 0:
                    a = randint(-60,t/2)
                    b = randint(-60,t/2)
                    if (a == b):
                        if bidomatic.bids_left > 0:
                            if bidomatic.win and auction.last_bid_type == 'm':
                                pass
                            else:
                                bidomatic.bid(auction)
                """

                if auction.time_left < 0:
                    auction.end()
                    flush_transaction()
                    ## automatically rotation loop (creates new auction for funding)
                    ## if auction is already there don't create it
                    # if Auction.objects.waiting_pledge().count() < settings.MAX_AUCTIONS:
                    if not Auction.objects.showcase().filter(item__code=auction.item.code).exists():
                        amount = auction.item.amount
                        # don't create only if amount = 0
                        if amount != 0:
                            auction = Auction.objects.create_from_item(auction.item)



                    """
                    if bidomatic.win:
                        if  auction.last_bid_type == 'n':
                            if bidomatic.bids_left > 0:
                                bidomatic.bid(auction)
                                continue
                                #return False
                        else:
                            auction.end()
                            continue
                    if bidomatic.bids_left > 0:
                        bidomatic.bid(auction)
                        continue
                    auction.end()"""
            sleep(1)

"""
class Bidomatic(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.kill_received = False
    def run(self):
        while not self.kill_received:
            for auction in Auction.objects.running():
                t = auction.time_left
                bidomatic = auction.maticbid
                if t > 0:
                    a = randint(-60,t/2)
                    b = randint(-60,t/2)
                    if (a == b):
                        if bidomatic.bids_left > 0:
                            if bidomatic.win and auction.last_bid_type == 'm':
                                pass
                            else:
                                bidomatic.bid(auction)
                #else:
                #    bidomatic.bid(auction)

                if auction.time_left < 0:
                    if bidomatic.win:
                        if  auction.last_bid_type == 'n':
                            if bidomatic.bids_left > 0:
                                bidomatic.bid(auction)
                                continue
                                #return False
                        else:
                            auction.end()
                            continue
                    if bidomatic.bids_left > 0:
                        bidomatic.bid(auction)
                        continue
                    auction.end()
            sleep(1)
            """


class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.

    """
    def on_data(self, data):
        tweet = json.loads(data)
        try:
            profile = Member.objects.get(user__social_auth__provider='twitter',
                                     user__social_auth__uid=tweet['user']['id'])
            profile.points_amount += Member.rewards.twit
            profile.credits += member.rewards.bid_for_twit
            profile.save()
        except User.DoesNotExist:
            print 'no duch user' , tweet['user']['id']
        return True

    def on_error(self, status):
        print 'got error', status


threads = []
class Command(BaseCommand):
    def handle(self, **options):
        try:
            b = Bidomatic()
            b.start()
            d = Dispatcher()
            d.start()
            # c = UpdateCache()
            # c.start()
            #threads.extend([k, c, b])
            l = StdOutListener()
            auth = OAuthHandler(settings.TWITTER_CONSUMER_KEY,
                                settings.TWITTER_CONSUMER_SECRET)
            auth.set_access_token(settings.TWITTER_ACCESS_TOKEN,
                                  settings.TWITTER_TOKEN_SECRET)

            stream = Stream(auth, l)
            stream.filter(track=settings.TWITTER_HASH_TAGS, async=True)
            threads.extend([b, d])
            while True:
                raw_input()
        except (KeyboardInterrupt, SystemExit):
            for t in threads:
                t.kill_received = True
            stream.disconnect()

