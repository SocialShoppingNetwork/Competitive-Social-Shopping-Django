# -*- coding: utf-8 -*-

from decimal import Decimal
from json import dumps, loads
from collections import deque
from time import time
import weakref

import redis
import gevent
import datetime

from django.core.urlresolvers import reverse
from django.template import loader
from django.conf import settings

from socketio.namespace import BaseNamespace

from .decorators import login_required

from apps.auctions.models import Auction
from apps.auctions.exceptions import *
from apps.auctions import constants
from settings.apps_settings import TRANSITION_PHASE_1_TIME
from apps.utils.mongo_connection import get_mongodb


redis_pool = redis.ConnectionPool(host=settings.REDIS['host'],
                                  port=settings.REDIS['port'],
                                  password=settings.REDIS['password'],
                                  db=0, max_connections=3)


def listener():
    "listens to redis server for new messages and distributes them to all sockets in current process"
    r = redis.StrictRedis(connection_pool=redis_pool)
    r = r.pubsub()
    r.subscribe('chat')
    r.subscribe('auction')
    for message in r.listen():
        if message['type'] != 'message':continue
        print 'got message from redis', message
        data = loads(message['data'])
        pkt = dict(type="event",
                   name=data['event'],
                   args=data['args'])
        if message['channel'] == 'chat':
            klass = ChatNamespace
        elif message['channel'] == 'auction':
            klass = AuctionNamespace

        for ref in klass.instances:
            instance = ref()
            if instance is not None:
                pkt['endpoint'] = instance.ns_name
                instance.socket.send_packet(pkt)


gevent.spawn(listener)


def automessage():
    while True:
        try:
            empty_refs = set()
            for ref in ChatNamespace.instances:
                instance = ref()
                if instance is not None:
                    if instance.request.user.is_authenticated:
                        message = "Invite your Facebook friends to join and receive points.<br>"\
                                "Collect points by being socially active on Exhibia, "\
                                "and use points to redeem prizes on Exhibia Reward Store"
                    else:
                        message = 'Welcome to Exhibia! Signup now and receive free bids.'
                    instance.emit('notification', message)
                else:
                    empty_refs.add(ref)
            # clean up empty refs
            if empty_refs:
                for ref in empty_refs:
                    ChatNamespace.instances.remove(ref)
                empty_refs = set()

        except SystemExit:
            break
        except Exception, e:
            print e
        gevent.sleep(settings.AUTOMESSAGE_DELAY)

gevent.spawn(automessage)


class RedisBroadcast(object):

    def initialize(self):
        self.instances.add(weakref.ref(self))

    def publish(self, event, *args):
        r = redis.Redis(connection_pool=redis_pool)
        msg = {'event':event, 'args':args}
        r.publish(self.channel, dumps(msg))


# chat_history = deque(maxlen=15)


class ChatNamespace(RedisBroadcast, BaseNamespace):
    instances = set()
    channel = 'chat'

    def initialize(self):
        super(ChatNamespace, self).initialize()
        if self.request.user.is_authenticated():
            self.session['username'] = self.request.user.username
            self.session['user_id'] = self.request.user.id
            self.session['avatar'] = self.request.user.profile.img_url
        else:
            self.session['username'] = u'guest'
            self.session['avatar'] = '' # pick default avatar
            self.session['user_id'] = '' # pick default avatar

    def on_send_chat_message(self, msg):
        r = redis.Redis(connection_pool=redis_pool)
        # if r.sinter('banned_users', self.session['username']):
        #     return
        # check if user is not banned
        # if self.session['user_id']:
        #     return

        message = [self.session['username'], msg[:200], self.session['avatar']]
        # first publish
        self.publish('user_message',  *message)
        # then add to MongoDB
        db = get_mongodb()
        db.chat.save({"username": self.session['username'],
                      "user_id": self.session['user_id'],
                      "avatar": self.session['avatar'],
                      "message": msg[:200],
                      "date": datetime.datetime.utcnow(),
                      })


class AuctionNamespace(RedisBroadcast, BaseNamespace):
    instances = set()
    channel = 'auction'

    @login_required
    def on_fund(self, message):
        print message
        try:
            auction = Auction.objects.select_related('item').get(pk=message['auction_pk'])
        except Auction.DoesNotExist:
            return
        member = self.request.user.profile
        amount = Decimal(message['amount'])
        member.pledge(auction, amount)
        member.incr_credits(amount)

        if auction.amount_pleged < auction.item.price:
            self.publish("auction_funded", auction.pk, '%.1f' % auction.amount_pleged,
                        auction.backers, '%.1f' %auction.funded)
        else:
            auction.status = constants.TRANSITION_PHASE_1
            auction.last_unixtime = time()
            auction.save()

            # notify all users, that have funded this item via facebook messages, google, mail
            for member in auction.backers_history:
                member.auction_funded_notify(message='Item %s was fully funded. '
                    'Exhibition will start in %s minutes!' % (auction.item.name, int(TRANSITION_PHASE_1_TIME/60)))

            self.publish("auction_funded", auction.pk, '%.1f' % auction.amount_pleged,
                        auction.backers, '%.1f' %auction.funded)



            ### it must be executed when timer of transition_phase_1 ends

            # if settings.MAX_AUCTIONS - Auction.objects.showcase().count() > 0:
            #     auction.status = constants.AUCTION_SHOWCASE
            #     auction.save()
            #     self.publish("auction_fund_ended", auction.pk, auction.time_left,
            #                  loader.render_to_string('auctions/showcase_box.html',
            #                  {'auction':auction,
            #                   'STATIC_URL':settings.STATIC_URL
            #                  }))
            # else:
            #     auction.in_queue = True
            #     auction.save()
            #     self.publish("auction_funded", auction.pk, '%.1f' % auction.amount_pleged,
            #         auction.backers, '%.1f' %auction.funded)

    def test(self):
        self.publish("auction_bid", 'auction.pk', 'auction.time_left',
                     'self.request.user.username', 'member.img_url')

    @login_required
    def on_bid(self, auction_pk):

        print 'BIIIID'
        member = self.request.user.profile
        if not auction_pk:
            return
        try:
            auction = Auction.objects.live().get(pk=int(auction_pk))
        except Auction.DoesNotExist:
            return

        try:
            member.bid(auction)

        except NotEnoughCredits:
            self.emit('NOT_ENOUGH_CREDITS')
        except AlreadyHighestBid:
            self.emit('ALREADY_HIGHEST_BID')
        except AuctionExpired:
            self.emit('AUCTION_EXPIRED')
        except AuctionLocked:
            self.emit('AUCTION_LOCKED')
        else:
            self.publish("auction_bid", auction.pk, auction.time_left,
                         self.request.user.username, member.img_url)

