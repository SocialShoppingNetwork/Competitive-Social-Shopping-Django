from django.core.management.base import BaseCommand
from django.core.cache import cache
from time import sleep, time
from auctions.models import Auction, AuctionItem
from auctions.constants import *
from django.db.models import F

from random import randint
from django.conf import settings
import threading
import cjson
from pprint import pprint

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

class KickOff(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.kill_received = False
    def run(self):
        while not self.kill_received:
            if Auction.objects.waiting_pledge().count() < settings.MAX_AUCTIONS:
                item = AuctionItem.objects.kick_off()
                auction = Auction.objects.create_from_item(item)
                #item.maticbid.create_auction_maticbid(auction)
                print 'kickoff auction : %s' % auction
            Auction.objects.finish_expired()
            sleep(5)

class Dispatcher(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.kill_received = False

    def run(self):
        while not self.kill_received:
            now = time()
            auctions_time_over = Auction.objects.time_over()
            if auctions_time_over:
                auctions_funded = auctions_time_over.filter(amount_pleged__gte=F('item__price'))
                auctions_funded.update(status=AUCTION_SHOWCASE)

                #auctions_not_funded = Auction.objects.filter(amount_pleged__lt=F('item__price'))
                #auctions_not_funded.update(status=AUCTION_FINISHED_NO_PLEDGED)

            if Auction.objects.waiting_pledge().count() < settings.MAX_AUCTIONS:
                item = AuctionItem.objects.kick_off()
                auction = Auction.objects.create_from_item(item)
                print 'kickoff auction : %s' % auction
            Auction.objects.finish_expired()
            sleep(5)


class Bidomatic(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.kill_received = False
    def run(self):
        while not self.kill_received:
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
            threads.extend([b, d])
            while True:
                r = raw_input()
        except KeyboardInterrupt:
            for t in threads:
                t.kill_received = True

