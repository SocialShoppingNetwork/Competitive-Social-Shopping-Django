# -*- coding: utf-8 -*-

import logging
from django.conf.urls.defaults import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from socketio import socketio_manage


from .namespaces import ChatNamespace, AuctionNamespace


NS = {
    '/auction':AuctionNamespace,
    '/chat': ChatNamespace,
}

@csrf_exempt
def socketio(request):
    try:
        # socketio_manage(request.environ, SOCKETIO_NS, request)
        socketio_manage(request.environ, NS, request)
    except:
        logging.getLogger("socketio").error("Exception while handling socketio connection", exc_info=True)
    return HttpResponse("")
