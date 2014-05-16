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
        result['a_%s' % a.id] = to_json(a)
    return result


class KillReceived(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(KillReceived, self).__init__(*args, **kwargs)
        self.kill_received = False


class KickOff(KillReceived):

    def run(self):
        while not self.kill_received:

            flush_transaction()
            ## checking time of transition phase 1
            for auction in Auction.objects.transition_phase_1():
                print '--->>> there are some auctions in transition phase 1 \n'
                if time() > auction.last_unixtime + settings.TRANSITION_PHASE_1_TIME:
                    auction.in_queue = True
                    auction.status = constants.AUCTION_WAITING
                    auction.last_unixtime = None
                    auction.save()
                    print '--->>> move from transition phase 1 to queue \n'

            ## checking time of transition phase 2
            for auction in Auction.objects.transition_phase_2():
                print '--->>> there are some auctions in transition phase 2 \n'
                if time() > auction.last_unixtime + settings.TRANSITION_PHASE_2_TIME:
                    auction.end()
                    print '--->>> move from transition phase 2 to queue \n'

            sleep(1)


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
                    ids = Auction.objects.waiting_pledge().filter(in_queue=True).values_list('pk', flat=True)[:available_slots]
                    Auction.objects.filter(pk__in=list(ids)).update(in_queue=False, status=constants.AUCTION_SHOWCASE)

            # if Auction.objects.showcase().count() < settings.MAX_AUCTIONS:
            #     item = AuctionItem.objects.get_giveaway_item()
            #     if item:
            #         Auction.objects.create_giveaway_from_item(item)
            #         print '--->>> add giveaway auction \n'

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
            ## changes items, wich were fully funded, to transition_phase_1
            if auctions_time_over:
                auctions_funded = auctions_time_over.filter(amount_pleged__gte=F('item__price'))
                auctions_funded.update(status=TRANSITION_PHASE_1)

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
                    auction.transition_phase_2()
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
            k = KickOff()
            k.start()
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

