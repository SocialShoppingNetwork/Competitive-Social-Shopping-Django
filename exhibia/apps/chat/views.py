from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from annoying.functions import get_object_or_None
from annoying.decorators import render_to, ajax_request
from django.contrib.auth.decorators import login_required
import cjson
from utils import post
from django.conf import settings

@csrf_exempt
def send_message(request):
    if request.user.is_authenticated():
        #TODO improve this part and just get the fields needed
        member = request.user.get_profile()
        if member.is_banned:
            return HttpResponseBadRequest()
        data = cjson.decode(request.read())
        message = data['message']
        if len(message)>255:
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
    username = request.POST.get('username')
    user = get_object_or_404(User, username__exact=username)
    profile = user.get_profile()
    profile.is_banned = True
    profile.save()
    post('http://' + settings.SOCKETIO_SERVER +'/ban-user/', {'username':username})
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


