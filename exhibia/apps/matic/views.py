from random import randint, choice
import cjson
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, get_object_or_404, render_to_response
from django.core.cache import cache
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt

from annoying.functions import get_object_or_None
from annoying.decorators import render_to, ajax_request

from auctions.models import Auction

@staff_member_required
@render_to('matic/admin.html')
def admin_index(request):
    auctions = Auction.objects.public()
    print auctions
    return {'auctions': auctions}

def to_json(auction):
    return {'id': auction.id,
            'status': auction.status,
            'last_bidder': auction.last_bidder,
            'time_left': auction.time_left,
            'bidding_time': auction.bidding_time,
            }

def auctions_to_json(auctions):
    result = {}
    for a in auctions:
        result['a_%s' % a.id] =  to_json(a)
    #print result
    return result

from utils import auction_to_dict, auctions_to_dict, admin_auctions_to_dict

@staff_member_required
@csrf_exempt
def auctions_status(request):
    auctions = Auction.objects.public()
    return HttpResponse(cjson.encode(admin_auctions_to_dict(auctions)))
@staff_member_required
@csrf_exempt
def change_tick_time(request, auction_id):
    #TODO check how to update using 'update'
    auction = get_object_or_404(Auction, id=auction_id)
    time = request.POST.get('time', auction.bidding_time)
    auction.bidding_time = time
    auction.save()
    return HttpResponse('OK')


@staff_member_required
@csrf_exempt
def pause_resume(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    if auction.is_paused:
        auction.resume()
    else:
        auction.pause()
    return HttpResponse("OK")

@staff_member_required
@csrf_exempt
def change_bidding_time(request, auction_id, seconds):
    auction = get_object_or_404(Auction, id=auction_id)
    auction.bidding_time = seconds
    auction.save()
    return HttpResponse("OK")

@staff_member_required
@csrf_exempt
def bid(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    bot = Bot.objects.all().order_by('?')[0]
    bot.bid(auction)
    return HttpResponse("OK")


@staff_member_required
@csrf_exempt
def pause_all(request):
    auctions = Auction.objects.live().select_related('item')
    print auctions,'PAUSE'
    for a in auctions:
        a.pause()
    return HttpResponse("OK")


@staff_member_required
@csrf_exempt
def resume_all(request):
    auctions = Auction.objects.live().select_related('item')
    for a in auctions:
        a.resume()
    return HttpResponse("OK")
