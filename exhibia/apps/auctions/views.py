# -*- coding: utf-8 -*-
import pymongo
import datetime
import cjson
from operator import attrgetter
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.views.decorators.csrf import csrf_exempt
from annoying.decorators import render_to, ajax_request
from utils import auction_to_dict, auctions_to_dict
from auctions.models import Auction, AuctionItem, AuctionBid
from auctions.exceptions import AlreadyHighestBid, AuctionExpired, AuctionIsNotReadyYet, NotEnoughCredits
from auctions.models import Category
from utils.mongo_connection import get_mongodb
from payments.forms import PledgeForm
from auctions.constants import AUCTION_FINISHED
from django.views.decorators.http import require_POST
from exhibia.settings import BID_REFUND_TIME


@csrf_exempt
@ajax_request
def bid_ajax(request, auction_id):
    user = request.user
    if not user.is_authenticated():
        return {'error': 'AUTH_REQUIRED'}
    auction = get_object_or_404(Auction, id=auction_id)
    member = user.get_profile()
    try:
        member.bid(auction)
    except NotEnoughCredits:
        return {'error': 'NOT_ENOUGH_CREDITS'}
    except AlreadyHighestBid:
        return {'error': 'ALREADY_HIGHEST_BID'}
    except AuctionExpired:
        return {'error': 'AUCTION_EXPIRED'}
    except AuctionIsNotReadyYet:
        return {'error': 'AUCTION_IS_NOT_READY_YET'}
    except Exception, e:
        print e
    else:
        return {'error': ''}


@csrf_exempt
@render_to('index_verstka.html')
def index(request):
    # auctions = Auction.objects.waiting_pledge().filter(item__categories=Category.objects.all()[0])
    auctions = Auction.objects.waiting_pledge() | Auction.objects.transition_phase_1()
    showcase = Auction.objects.live()

    # here we'll be storing those auctions in which user lost, but he still can get his bids back
    auctions_with_bid_return = (
        Auction.objects.finished()
        .filter(bids__bidder=request.user)
        .exclude(last_bidder_member=request.user)
        .annotate(bid_refund=Count('id'))
        .extra(select={'refund_time_left': 'FLOOR({}-(UNIX_TIMESTAMP()-ended_unixtime))'.format(BID_REFUND_TIME)})
        .extra(where=['UNIX_TIMESTAMP() - ended_unixtime < {}'.format(BID_REFUND_TIME)])
        .distinct()
        .select_related('item', 'item__image')
    ) if request.user.is_authenticated() else None

    if request.user.is_authenticated():
        for order in request.user.orders.all():
            print order.auction

    # auctions_with_bid_return = Auction.objects.raw("""
    #     SELECT a.id, COUNT(*) as bid_refund,
    #     FLOOR({bid_refund_time}-(UNIX_TIMESTAMP()-a.ended_unixtime)) as refund_time_left
    #     FROM auctions_auction a
    #     INNER JOIN auctions_auctionbid b ON b.auction_id=a.id
    #     INNER JOIN auth_user u ON b.bidder_id=u.id
    #     WHERE a.status = {status!r} AND u.id = {user_id} AND a.last_bidder_member_id <> {user_id}
    #     AND UNIX_TIMESTAMP() - a.ended_unixtime < {bid_refund_time}
    #     GROUP BY a.id
    # """.format(status=AUCTION_FINISHED, user_id=request.user.pk,
    #            bid_refund_time=BID_REFUND_TIME)) if request.user.is_authenticated() else None

    auctions_ended = Auction.objects.finished().select_related('item', 'item__image')[:4]
    items = Auction.objects.public().order_by('created').select_related('item', 'item__image')

    categories = Category.objects.all()


    # last 15 chat messages from mongo
    db = get_mongodb()
    chat_messages = list(db.chat.find().sort("date", pymongo.DESCENDING).limit(15))
    chat_messages.reverse()

    return {'auctions': auctions.filter(item__categories=Category.objects.all()[0]),
            'showcase': showcase,
            'items': showcase,
            'categories': categories,
            'auctions_with_bid_return': auctions_with_bid_return,
            'messages': chat_messages,
            'auctions_ended q': auctions_ended}


def xauction_bid(request, auction_id):
    pass


@render_to('auctions/item_exhibit.html')
def view_item(request, slug):
    try:
        item = AuctionItem.objects.select_related('auctions').get(slug_name=slug)
    except AuctionItem.DoesNotExist:
        raise Http404('no such item')
    auction = None
    auctions = list(item.auctions.all())
    if auctions:
        auctions.sort(key=attrgetter('created'))
        auction = auctions[0]
    result = {'auction': auction,
              'backers': '',
              'item': item,
              'd': datetime.datetime.now()}

    if auction:
        result['backers'] = auction.backers_history
        result['bidding_history'] = auction.bidding_history
    return result


@render_to('buy_now.html')
def buy_now(request, item_id):
    return {}


def auction_bid(request, auction_id=None):
    "not used"
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('acct_login')) #TODO redirect to register
        #member = request.member
    member = request.user.get_profile()
    if auction_id is None:
        auction_id = request.POST.get('auction_id', None)
        if auction_id:
            auction = get_object_or_404(Auction.objects.live(), id=auction_id)
        else:
            raise Http404
    else:
        auction = get_object_or_404(Auction.objects.live(), pk=auction_id) #change it
    try:
        result = member.bid(auction)
    except NotEnoughCredits:
        return HttpResponseRedirect(reverse('buycredits'))
    except AlreadyHighestBid:
        messages.add_message(request, messages.ERROR, 'Already HighestBidder')
    except AuctionExpired:
        messages.add_message(request, messages.ERROR, 'Auction Expired')
    return HttpResponseRedirect(reverse('auction_item', args=[slugify(auction.item.name)]) + '?auction=%s' % auction.id)


@csrf_exempt
@render_to('auctions/auctions.html')
def get_auctions(request):
    items_ids = request.POST.getlist('items[]')
    print items_ids
    items = Auction.objects.public().filter(id__in=items_ids)
    print items
    return {'items': items, 'hide_header': True}


@csrf_exempt
def fund(request, auction_id):
    # not used anymore. see streamer.namespaces
    if not request.user.is_authenticated():
        if request.is_ajax():
            response = {'error': "AUTH_REQUIRED"}
            return HttpResponse(cjson.encode(response))
        return HttpResponseRedirect(reverse('acct_login')) #TODO redirect to register
    auction = get_object_or_404(Auction, id=auction_id)
    member = request.user.get_profile()
    amount = int(float(request.POST['amount']))
    member.pledge(auction, amount)
    member.incr_credits(amount)
    if request.is_ajax():
        response = {'response': 'OK'}
        return HttpResponse(cjson.encode(response))
    else:
        return HttpResponseRedirect('/')


@csrf_exempt
def auction_info(request, auction_id):
    auction = [get_object_or_404(Auction, id=auction_id)]
    return HttpResponse(cjson.encode(auctions_to_dict(auction)))


@csrf_exempt
def auctions_info(request):
    auctions = Auction.objects.waiting_pledge()
    return HttpResponse(cjson.encode(auctions_to_dict(auctions)))




@render_to('payments/pledge.html')
def pledge(request, item_id):
    auction = get_object_or_404(Auction, id=item_id)
    form = PledgeForm(initial={'auction': auction.id})
    return {'auction': auction,
            'form': form}


@render_to('fb/checkout.html')
@login_required
def checkout(request):
    member = request.user.get_profile()
    pay_shipping_fees = Auction.objects.filter(last_bidder_member=member)
    return {}


@csrf_exempt
def append_funding_carousel(request):
    category_id = request.GET.get('category_id')
    auctions = Auction.objects.waiting_pledge() | Auction.objects.transition_phase_1()
    auctions = auctions.filter(item__categories=category_id)
    if not auctions:
        return HttpResponse('')
    return render(request, 'auctions/funding_carousel_verstka.html', {'auctions': auctions})


@csrf_exempt
@require_POST
def append_battle_modal(request):
    try:
        auction = (Auction.objects.select_related('item', 'item__image', 'bids', 'bids__bidder')
                   .get(pk=request.POST.get('id')))
    except Auction.DoesNotExist:
        return HttpResponse('')
    latest_bids = AuctionBid.objects.filter(auction=auction).order_by('-id')[:6]
    return render(request, 'auctions/modal_battle.html', {'auction': auction, 'latest_bids': latest_bids})
