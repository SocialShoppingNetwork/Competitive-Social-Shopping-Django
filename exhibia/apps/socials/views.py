import datetime
import cjson
import settings

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, get_object_or_404, render_to_response
from django.core.cache import cache
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from annoying.functions import get_object_or_None
from annoying.decorators import render_to, ajax_request

from auctions.models import Auction, AuctionItem
from socials.models import LikeItem

@csrf_exempt
@login_required
def reward_like_item(request):
    if 'google' in request.GET:
        type = 'G'
        limit = settings.GOOGLEPLUS_ITEM_LIMIT_DAILY
        #transaction_type = 'GLI'
        free_bids = settings.GOOGLEPLUS_ITEM_FREEBIDS
    else: #Facebook
        type = 'F'
        limit = settings.FACEBOOK_LIKES_ITEM_LIMIT_DAILY
        #transaction_type = 'FLI'
        free_bids = settings.FACEBOOK_LIKE_ITEM_FREEBIDS

    today = datetime.date.today()
    item_code = request.POST.get("item_code")
    member = request.user.get_profile()

    try:
        item = get_object_or_404(AuctionItem, code=item_code)
        like = get_object_or_None(LikeItem, item=item, member=member, type=type)
        if like:
            response = cjson.encode({'error':'ALREADY_LIKE'})
            return HttpResponse(response, mimetype="application/json")
        else:
            likes = LikeItem.objects.filter(member=member,
                                            created__day=today.day,
                                            created__month=today.month,
                                            created__year=today.year,
                                            type=type)
            if likes.count() >= limit:
                response = cjson.encode({'error':'LIKE_LIMIT'})
                return HttpResponse(response, mimetype="application/json")
            item = LikeItem.objects.create(item=item, member=member, type=type)
            return HttpResponse("OK")
    except AuctionItem.DoesNotExist:
        response = cjson.encode({'error':'ITEM_DOES_NOT_EXIST'})
        return HttpResponse(response, mimetype="application/json")

