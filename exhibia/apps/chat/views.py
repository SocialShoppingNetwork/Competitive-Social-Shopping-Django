from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect
from django.conf import settings
from django.contrib import messages

from annoying.functions import get_object_or_None
from annoying.decorators import render_to, ajax_request
import cjson
from utils import post
import redis
from apps.utils.mongo_connection import get_mongodb
import pymongo
from bson.objectid import ObjectId


@csrf_exempt
def send_message(request):
    if request.user.is_authenticated():
        #TODO improve this part and just get the fields needed
        member = request.user.get_profile()
        if member.is_banned:
            return HttpResponseBadRequest()
        data = cjson.decode(request.read())
        message = data['message']
        if len(message) > 255:
            return HttpResponseBadRequest()
        data = {'username':request.member.user.username,
                'message':message,
                'picture':request.member.img_url
        }
        post('http://' + settings.SOCKETIO_SERVER +'/message/', data)
        return HttpResponse('OK')
    return HttpResponseBadRequest()


@user_passes_test(lambda u: u.is_staff)
@csrf_exempt
def ban_user(request):
    id = request.POST.get('user_id')
    user = User.objects.get(pk=id)
    profile = user.get_profile()
    status = int(request.POST.get('status'))
    print 'JS status %s' % status
    print 'profiled was %s' % profile.is_banned
    profile.is_banned = 1 - status
    print 'profiled become %s' % profile.is_banned
    profile.save()

    return HttpResponse('OK')

@user_passes_test(lambda u: u.is_staff)
@csrf_exempt
def unban_user(request):
    username = request.POST.get('username')
    user = get_object_or_404(User, username__exact=username)
    profile = user.get_profile()
    profile.is_banned = False
    profile.save()
    return HttpResponse('OK')


@staff_member_required
@render_to('chat/admin_list.html')
def admin_chat(request):

    db = get_mongodb()

    if request.method == 'POST':
        if request.POST.get('action') == 'delete_selected':
            ids = request.POST.getlist('_selected_action')
            if ids:
                response = db.chat.remove({"_id": {"$in": [ObjectId(id) for id in ids]}})
                if response.get('err') is None:
                    messages.add_message(request, messages.INFO, 'Successfully deleted %s message.' % response.get('n', 0))
                    return redirect('admin_chat')
            else:
                messages.add_message(request, messages.INFO, 'Items must be selected in order to perform actions on them. No items have been changed.')
        elif not request.POST.get('action'):
            messages.add_message(request, messages.INFO, 'No action selected.')

    # chat_messages = list(db.chat.find().limit(15).sort("date", pymongo.DESCENDING))
    cursor = db.chat.find().limit(15).sort("date", pymongo.DESCENDING)

    chat_messages = []
    users = dict()

    for message in cursor:
        if not message['user_id']:
            message['user'] = None
        else:
            message['user'] = users.get(message['user_id'], User.objects.get(pk=message['user_id']))
        chat_messages.append(message)

    return {
        'chat_messages': chat_messages,
    }



