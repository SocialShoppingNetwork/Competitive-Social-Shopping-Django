# -*- coding: utf-8 -*-

from decimal import Decimal
from json import dumps, loads
from collections import deque
import weakref

import redis
import gevent

from django.core.urlresolvers import reverse
from django.template import loader
from django.conf import settings

from socketio.namespace import BaseNamespace

from .decorators import login_required

from auctions.models import Auction
from auctions.exceptions import *
from auctions import constants


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

chat_history = deque(maxlen=15)


class ChatNamespace(RedisBroadcast, BaseNamespace):
    instances = set()
    channel = 'chat'

    def initialize(self):
        super(ChatNamespace, self).initialize()
        if self.request.user.is_authenticated():
            self.session['username'] = self.request.user.username
            self.session['avatar'] = self.request.user.profile.img_url
        else:
            self.session['username'] = u'guest'
            self.session['avatar'] = '' # pick default avatar
        for i in chat_history:
            self.emit('user_message', *i)


    def on_send_chat_message(self, msg):
        r = redis.Redis(connection_pool=redis_pool)
        if r.sinter('banned_users', self.session['username']):
            return
        message = [self.session['username'], msg[:200], self.session['avatar']]
        chat_history.append(message)
        self.publish('user_message',  *message)


class AuctionNamespace(RedisBroadcast, BaseNamespace):
    instances = set()
    channel = 'auction'

    @login_required
    def on_fund(self, message):
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
            if settings.MAX_AUCTIONS - Auction.objects.showcase().count() > 0:
                auction.status = constants.AUCTION_SHOWCASE
                auction.save()
                self.publish("auction_fund_ended", auction.pk, auction.time_left,
                             loader.render_to_string('auctions/showcase_box.html',
                             {'auction':auction,
                              'STATIC_URL':settings.STATIC_URL
                             }))
            else:
                # TODO: correct html update
                # TODO: add items form queue
                auction.in_queue = True
                auction.save()
                print 'ON_FUND!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! LOLOLOLOLOL'
                self.publish("auction_funded", auction.pk, '%.1f' % auction.amount_pleged,
                    auction.backers, '%.1f' %auction.funded)


    @login_required
    def on_bid(self, auction_pk):
        member = self.request.user.profile
        if not auction_pk:
            return
        try:
            auction = Auction.objects.live().get(pk=int(auction_pk))
        except Auction.DoesNotExist: return
        try:
            member.bid(auction)
        except NotEnoughCredits:
            self.emit('NOT_ENOUGH_CREDITS')
        except AlreadyHighestBid:
            self.emit('ALREADY_HIGHEST_BID')
        except AuctionExpired:
            self.emit('AUCTION_EXPIRED')
        else:
            self.publish("auction_bid", auction.pk, auction.time_left,
                         self.request.user.username, member.img_url)

