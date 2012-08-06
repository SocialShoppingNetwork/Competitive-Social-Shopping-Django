from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
from annoying.functions import get_object_or_None
from annoying.decorators import render_to, ajax_request
from django.contrib.auth.decorators import login_required
import cjson

@csrf_exempt
def send_message(request):
    if request.member:
        data = cjson.decode(request.read())
        message = data['message']
        if len(message)>255:
            return HttpResponseBadRequest()
        data = {'user':request.member.user.username,
                'message':message,
                'picture':request.member.img_url}
        
        return HttpResponse()
    return HttpResponseBadRequest()