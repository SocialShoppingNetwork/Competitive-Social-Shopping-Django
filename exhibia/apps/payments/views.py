from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, get_object_or_404, render_to_response
from django.core.cache import cache
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from annoying.functions import get_object_or_None
from annoying.decorators import render_to, ajax_request
from django.views.decorators.csrf import csrf_exempt

#from payments.gateways.plimus import PlimusGateway
from payments.gateways.dalpay import DalpayGateway

from payments.models import CreditPackageOrder
from payments.constants import *
from profiles.models import Member

import settings

def create_gateway(pay_method, *args, **kwargs):
    """Package could be an AuctionOrder or CreditPackage"""
    if pay_method not in settings.PAYMENTS_GATEWAY:
        raise Http404
    currency = "USD" #TODO check this
#    if pay_method == 'plimus':
#        gateway = PlimusGateway({
#            'call_url': settings.PLIMUS_CALL_URL,
#            'test_mode': settings.TEST_MODE,
#            'function': kwargs['function'],
#            'currency': currency,
#        })
    if pay_method == 'dalpay':
        gateway = DalpayGateway({
            'call_url': settings.DALPAY_CALL_URL,
            'test_mode': settings.TEST_MODE,
            'function': kwargs['function'],
            'currency': currency,
        })
    else:
        raise PaymentGatewayNotImplemented
    return gateway

def package_form(request, pay_method):
    gateway = create_gateway(pay_method,
                             custom1=request.user.username,
                             function='credits')
    params = {'gateway': gateway,}
    c = RequestContext(request, params)
    return render_to_string('payments/package_form_%s.html' % pay_method,  context_instance=c)


@login_required
def buycredits(request, template_name='payments/buycredits.html'):
    return
#    """First Step"""
#    packages = CreditPackage.objects.order_by('credits')
#    if request.is_ajax():
#        template_name='payments/buycredits_ajax.html'
#    forms = [package_form(request, 'dalpay', p.code) for p in packages]
#    c = RequestContext(request, {
#        "packages": packages,
#        "forms" : forms,
#    })
#    return render_to_response(template_name, context_instance=c)

def order_dalpay(request, kind, handler):
    assert kind == CREDITS or kind == AUCTION
    if request.method == 'POST':
        gateway = DalpayGateway({'function': kind,})
        data = dict(request.POST.items())
        return gateway.call(request, data, handler)
    else:
        return HttpResponse('')

def credits_dalpay_handler(request, data, pn, extra):
    #f = open(settings.DEBUG_FILE + str(time()), 'w')
    #f.write('package_order_plimus_handler: pn -> %s, pn.confirm -> %s\n' % (pn, pn.confirm))
    assert pn.function == CREDITS
    if pn.confirm == CONFIRMED:
        order = CreditPackageOrder(buyer=buyer,
                                   amount_paid=float(pn.mc_gross),
                                   status=pn.status,
                                   pn=pn)
                                   #TODO item = models.ForeignKey('auctions.AuctionItem', blank=True, null=True)
        order.save()

def auction_dalpay_handler(request, data, pn, extra):
    #f = open(settings.DEBUG_FILE + str(time()), 'w')
    #f.write('auction_order_plimus_handler: pn -> %s, mc_gross -> %s\n' % (pn, pn.mc_gross))
    assert pn.function == AUCTION
    try:
        order = AuctionOrder.objects.get(pk=pn.item_number, winner__user__username=pn.custom1, status="n", pn__isnull=True)
        order.pn = pn
        order.method = 'p' #ORDER_PAID
        order.save()
        #f.write('auction_order_plimus_handler: order: %s %s, float(pn.mc_gross) >= order.total? %s\n' % (order, order.status, float(pn.mc_gross) >= order.total))
        # AUCTION ORDER
        if float(pn.mc_gross) >= order.auction.item.shipping_fee:
            if order.status != ORDER_PAID:
                order.auction.status = "d" #AUCTION_PAID
                order.auction.save()
                order.status = ORDER_PAID
                order.save()
        else:
            order.status = ORDER_SUSPENDED
            order.save()
        f.close()
    except AuctionOrder.DoesNotExist:
        #f.close()
        #raise DoesNotFindOrder
        pass

@csrf_exempt
def package_order_dalpay(request):
    return order_dalpay(request, CREDITS, credits_dalpay_handler)

@csrf_exempt
def auction_order_dalpay(request):
    return order_dalpay(request, AUCTION, auction_dalpay_handler)
