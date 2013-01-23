# -*- coding: utf-8 -*-


import datetime
import json
import cjson
import settings

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_list_or_404, get_object_or_404, render_to_response, redirect
from django.core.cache import cache
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from annoying.functions import get_object_or_None
from annoying.decorators import render_to, ajax_request
from social_auth.views import complete

from auctions.models import Auction, AuctionItem
from socials.models import LikeItem, Invitation

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


def registration_complete(request, *args, **kwargs):
    "this might be not a registration but invited user redirected from e.g. facebook"
    if request.GET:
        if 'request_ids' in request.GET:
            # this is a request from invitation from facebook
            request_ids = request.GET['request_ids'].split(',')
            request.session['invited_via'] = 'facebook'
            request.session['invitation_ids'] = request_ids
            print 'setting session'
            return redirect(reverse("acct_login")) # or maybe some invitation greetings

    # at this point user almost registered so we need to check for invitations in session
    if 'invited_via' in request.session:
        invitation_ids = request.session['invitation_ids']
        users = User.objects.filter(invitations__external_id__in=invitation_ids)
        for user in users:
            user.get_profile().invitation_succeed()
        try:
            del request.session['invitation_ids']
            del request.session['invited_via']
        except:pass
    return complete(request, *args, **kwargs)


@login_required
@csrf_exempt
def add_invitation(request):
    if request.is_ajax():
        req_id = request.POST.get('request')
        if req_id:
            for id in req_id.split(","):
                Invitation.objects.create(user=request.user, external_id=id)
            return HttpResponse('ok')
        return HttpResponse('no ids')
    return redirect(reverse('home'))



def user_like(request):
    if not request.user.is_authenticated():
        return HttpResponse('')
    like_source = request.GET.get('type', None)
    known_providers = request.user.social_auth.all().values_list('provider', flat=True)
    if not like_source or like_source not in known_providers:
        return HttpResponse('')
    request.user.get_profile().like(request.GET['href'], like_source)
    return HttpResponse('ok')



