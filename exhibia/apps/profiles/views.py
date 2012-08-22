from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.template import RequestContext
from django.shortcuts import get_list_or_404, get_object_or_404, render_to_response

from annoying.functions import get_object_or_None
from annoying.decorators import render_to, ajax_request

from auctions.models import Auction
from auctions.exceptions import AlreadyHighestBid, AuctionExpired, AuctionIsNotReadyYet, NotEnoughCredits

#from profiles.forms import MemberInfoFormUS
from payments.models import AuctionOrder
from payments.constants import *


from shipping.forms import ShippingForm
from shipping.models import ShippingAddress

@login_required
def auctions_won(request, template_name='profiles/auctions_won.html'):
    member = request.member
    auctionorders_unpaid = AuctionOrder.objects.filter(status=ORDER_NOT_PAID, winner=member)
    auctions_won = Auction.objects.filter(status="f", last_bidder_member=member).order_by("-last_unixtime")
    c = RequestContext(request, {
        "member": member,
        "auctionorders_unpaid": auctionorders_unpaid,
        "auctions_won": auctions_won,
    })
    return render_to_response(template_name, context_instance=c)

from payments.models import AuctionOrder
@login_required
def auction_won(request, auction_id, template_name='profiles/auction_won.html'):
    member = request.member
    auction = get_object_or_404(Auction, id=auction_id, last_bidder=member.user.username, status="f")
    if request.POST:
        confirm = request.POST.get('confirm', 'no')
        if confirm == "yes":
            order = AuctionOrder.objects.create_order(auction, member)
            return HttpResponseRedirect('/accounts/profile/won/')
    c = RequestContext(request, {"a": auction,
                                 "member": member,
                                 'shipping':member.shippingprofile,})
    return render_to_response(template_name, context_instance=c)

@login_required
def order_pay(request, order_id):
    member = request.member
    order = get_object_or_404(AuctionOrder, id=order_id, winner=member, auction__status="m")
    c = RequestContext(request, {
        "order": order,
        "dalpay_form": auction_form(request, 'dalpay', order_id),
    })
    return render_to_response('order_pay.html', context_instance=c)

@login_required
def member_info(request, template_name='profiles/member_info.html'):
    next_page = request.REQUEST.get('next')
    shipping = request.member.shippingprofile
    form_class = MemberInfoFormUS
    if request.POST:
        f = form_class(request.POST)
        if f.is_valid():
            data = f.cleaned_data
            shipping.first_name =  data['first_name']
            shipping.last_name = data['last_name']
            shipping.address1 = data['address1']
            shipping.address2 = data['address2']
            shipping.city = data['city']
            shipping.zip_code = data['zip_code']
            shipping.state = data['state']
            shipping.phone = data['phone']
            shipping.save()
            #member.user.save()
            if next_page:
                return HttpResponseRedirect(next_page)
            return HttpResponseRedirect(reverse('home'))
    else:
        f = form_class(initial={'first_name' : shipping.first_name,
                                'last_name' : shipping.last_name,
                                'address1' : shipping.address1,
                                'address2' : shipping.address2,
                                'city': shipping.city,
                                'zip_code' : shipping.zip_code,
                                'state' : shipping.state,
                                'phone' : shipping.phone
                                })
    c = RequestContext(request,{'f': f,
                                'member': request.member,
                                'next_page':next_page})
    return render_to_response(template_name, context_instance=c)

def member_bids(request):
    """ returns the number of bid of the current user """
    if not request.user.is_authenticated():
        return HttpResponse("0")
    return HttpResponse(str(request.member.credits))



ORDER_WAITING_PAYMENT = 'wp'
ORDER_SHIPPING_FEE_REQUESTED = 'rf'
ORDER_PROCESSING_ORDER = 'rf'
ORDER_PAID = 'pd' # Processing Order
ORDER_DELIVERED = 'dl'
ORDER_WAITING_TESTIMONIAL = 'wt'
from django.db.models import Q


from shipping.constants import ORDER_WAITING_PAYMENT, ORDER_SHIPPING_FEE_REQUESTED, ORDER_SHIPPED
@login_required
@render_to('profiles/account.html')
def account(request):
    member = request.user.get_profile()
    print member
    print '-----'
    #auctions_waiting_payment = member.items_won.filter(Q(shippingorder=None) |
    #                                            Q(shippingorder__status=ORDER_WAITING_PAYMENT) |
    #                                            Q(shippingorder__status=ORDER_SHIPPING_FEE_REQUESTED))
    auctions_waiting_payment = member.items_won.filter(order=None)
    print auctions_waiting_payment.count()
    #orders processing and shipped
    #auctions_processing_shipped = member.items_won.filter(Q(shippingorder__status=ORDER_PROCESSING_ORDER) |
    #                                             Q(shippingorder__status=ORDER_SHIPPED))
    auctions_processing_shipped = []
    auctions_record_testimonial = []
    #auctions_record_testimonial = member.items_won.filter(shippingorder__status=ORDER_SHIPPED, video=None)

    return {'member':member,
            'auctions_waiting_payment': auctions_waiting_payment,
            'orders_processing_shipped': auctions_processing_shipped,
            'orders_record_testimonial': auctions_record_testimonial,
    }

@login_required
@render_to('profiles/shipping.html')
def manage_shipping(request):
    member = request.user.get_profile()
    shipping_profiles = member.shippingaddress_set.filter(deleted=False)
    shipping = None
    id = request.GET.get('id')
    if 'delete' in request.GET:
        shipping = get_object_or_404(ShippingAddress, id=id, member=member)
        shipping.deleted = True
        shipping.save()
        return HttpResponseRedirect(reverse('account_shipping'))

    if request.method == 'POST':
        form = ShippingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if id:
                shipping = get_object_or_404(ShippingAddress, id=id, member=member)
                shipping.first_name =  data['first_name']
                shipping.last_name = data['last_name']
                shipping.address1 = data['address1']
                shipping.address2 = data['address2']
                shipping.city = data['city']
                shipping.zip_code = data['zip_code']
                shipping.country = data['country']
                shipping.state = data['state']
                shipping.phone = data['phone']
                shipping.save()
                return HttpResponseRedirect(reverse('account_shipping'))
            else:
                shipping = form.save(commit=False)
                shipping.member = member
                shipping.save()
                return HttpResponseRedirect(reverse('account_shipping'))
    else:
        if id:
            shipping = get_object_or_404(ShippingAddress, id=id, member=member)
            form = ShippingForm(initial=shipping.__dict__)
        else:
            form = ShippingForm()

    return {
        'form':form,
        'shipping_profiles':shipping_profiles,
        'shipping':shipping
    }

"""
* Pay Shipping Fee
* Waiting Shipping fee
* Processing Shipping
* Processing Order
* Post Testimonials
"""