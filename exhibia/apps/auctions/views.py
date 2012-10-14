import datetime
import cjson

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, get_object_or_404, render_to_response
from django.core.cache import cache
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseGone
from annoying.functions import get_object_or_None
from annoying.decorators import render_to, ajax_request

from auctions.models import Auction, AuctionItem
from auctions.exceptions import AlreadyHighestBid, AuctionExpired, AuctionIsNotReadyYet, NotEnoughCredits

@csrf_exempt
@ajax_request
def bid_ajax(request, auction_id):
    user = request.user
    if not user.is_authenticated():
        return {'error':'AUTH_REQUIRED'}
    auction = get_object_or_404(Auction, id=auction_id)
    member = user.get_profile()
    try:
        member.bid(auction)
    except NotEnoughCredits:
        return {'error':'NOT_ENOUGH_CREDITS'}
    except AlreadyHighestBid:
        return {'error':'ALREADY_HIGHEST_BID'}
    except AuctionExpired:
        return {'error':'AUCTION_EXPIRED'}
    except AuctionIsNotReadyYet:
        return {'error':'AUCTION_IS_NOT_READY_YET'}
    except Exception, e:
        print e
    else:
        return {'error':''}

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
@render_to('index.html')
def index(request):
    auctions = Auction.objects.waiting_pledge()
    #showcase = Auction.objects.showcase()
    showcase = Auction.objects.live()
    #auctions = cache.get('auctions')
    #auctions_json = cache.get('auctions_json')
    auctions_ended  = Auction.objects.finished().select_related('item', 'item__image')[:4]
    items = Auction.objects.public().order_by('created').select_related('item', 'item__image')
    return {'auctions': auctions,
            'showcase': showcase,
            'items':items,
            #'auctions_json': auctions_json,
            'auctions_ended q': auctions_ended}

def xauction_bid(request, auction_id):
    pass

@render_to('auctions/item_exhibit.html')
def view_item(request, slug=''):
    auction_id = request.GET.get('item')
    auction = None
    item = None
    if auction_id:
        try:
            auction = Auction.objects.select_related('item', 'item__image').get(pk=auction_id)
            #auction = get_object_or_404(Auction.objects.all(), pk=auction_id)
        except Auction.DoesNotExist:
            raise Http404
        item = auction.item
    else:
        item = AuctionItem.objects.select_related('item', 'item__image').get(slug_name__exact=slug)

    result = {'auction': auction,
              'backers':'',
              'item': item,
              'd':datetime.datetime.now()}

    if auction:
        result['backers'] = auction.backers_history
        result['bidding_history'] = auction.bidding_history
    return result

@render_to('buy_now.html')
def buy_now(request, item_id):
    return {}

def auction_bid(request, auction_id=None):
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
    return HttpResponseRedirect(reverse('auction_item', args=[slugify(auction.item.name)])+'?auction=%s' % auction.id)

@csrf_exempt
@render_to('auctions/auctions.html')
def get_auctions(request):
    items_ids = request.POST.getlist('items[]')
    print items_ids
    items = Auction.objects.public().filter(id__in=items_ids)
    print items
    return {'items':items, 'hide_header':True}


@csrf_exempt
def fund(request, auction_id):

    if not request.user.is_authenticated():
        if request.is_ajax():
            response = {'error':"AUTH_REQUIRED"}
            return HttpResponse(cjson.encode(response))
        return HttpResponseRedirect(reverse('acct_login')) #TODO redirect to register
    auction = get_object_or_404(Auction, id=auction_id)
    member = request.user.get_profile()
    amount = int(float(request.POST['amount']))
    member.pledge(auction, amount)
    member.incr_credits(amount)
    if request.is_ajax():
        response = {'response': 'OK'}
        return HttpResponse(cjson.encode(response));
    else:
        return HttpResponseRedirect('/')

from utils import auction_to_dict, auctions_to_dict
@csrf_exempt
def auction_info(request, auction_id):
    auction = [get_object_or_404(Auction, id=auction_id)]
    return HttpResponse(cjson.encode(auctions_to_dict(auction)))

@csrf_exempt
def auctions_info(request):
    auctions = Auction.objects.waiting_pledge()
    return HttpResponse(cjson.encode(auctions_to_dict(auctions)))



from payments.forms import PledgeForm
@render_to('payments/pledge.html')
def pledge(request, item_id):
    auction = get_object_or_404(Auction, id=item_id)
    form = PledgeForm(initial={'auction':auction.id})
    return {'auction':auction,
            'form':form}

@render_to('fb/checkout.html')
@login_required
def checkout(request):
    member = request.user.get_profile()
    pay_shipping_fees = Auction.objects.filter(last_bidder_member=member)
    return {}
