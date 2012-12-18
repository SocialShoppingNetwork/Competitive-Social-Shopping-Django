# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import get_list_or_404, get_object_or_404, render_to_response, redirect, render

from annoying.decorators import render_to

from auctions.models import Auction
from auctions.exceptions import AlreadyHighestBid, AuctionExpired, AuctionIsNotReadyYet, NotEnoughCredits

#from profiles.forms import MemberInfoFormUS
from payments.constants import *
from payments.models import Card
from payments.forms import CardForm
from shipping.forms import ShippingForm
from shipping.models import ShippingAddress
from profiles.models import BillingAddress
from profiles.forms import BillingForm, DeleteForm

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
ORDER_PROCESSING_ORDER = 'op'
ORDER_PAID = 'pd' # Processing Order
ORDER_DELIVERED = 'dl'
ORDER_WAITING_TESTIMONIAL = 'wt'

from shipping.constants import ORDER_WAITING_PAYMENT, ORDER_SHIPPING_FEE_REQUESTED, ORDER_SHIPPED, ORDER_PROCESSING


@login_required
@render_to('profiles/account.html')
def account(request):
    member = request.user.get_profile()
    #auctions_waiting_payment = member.items_won.filter(Q(shippingorder=None) |
    #                                            Q(shippingorder__status=ORDER_WAITING_PAYMENT) |
    #                                            Q(shippingorder__status=ORDER_SHIPPING_FEE_REQUESTED))
    auctions_waiting_payment = member.items_won.filter(order=None)


    #orders processing and shipped
    auctions_processing = member.items_won.filter(order__status=ORDER_PROCESSING)

    auctions_shipped = member.items_won.filter(order__status=ORDER_SHIPPED)
    return {'member':member,
            'auctions_waiting_payment': auctions_waiting_payment,
            'auctions_processing':auctions_processing,
            'auctions_shipped': auctions_shipped,
    }



@login_required
def manage_addresses(request, form_class=ShippingForm, redirect_url='account_shipping',
                    template='manage_shipping.html', user_attr='shipping_adddresses'):
    form = form_class(request.POST or None,
        initial={'first_name':request.user.first_name, 'last_name':request.user.last_name})
    if form.is_valid():
        shipping = form.save(False)
        shipping.user = request.user
        shipping.save()
        return redirect(reverse(redirect_url))
    return render(request, "profiles/"+template,
                  {'form':form,
                  'objects':getattr(request.user, user_attr).filter(deleted=False),
                  })

@login_required
def manage_delete(request, model=ShippingAddress, redirect_url='account_shipping'):
    if request.method != 'POST':
        raise Http404()
    form = DeleteForm(request.POST or None)
    if form.is_valid():
        try:
            obj = model.objects.get(user=request.user, pk=form.cleaned_data['pk'])
            obj.deleted = True
            obj.save()
        except Exception, e:print e
    return redirect(reverse(redirect_url))


@login_required
def manage_edit(request, pk, model=ShippingAddress, form=ShippingForm,
        redirect_url='account_shipping',template='profiles/manage_shipping.html'):
    obj = get_object_or_404(model, pk=pk)
    form = form(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect(redirect_url)
    return render(request, template,
                  {'form':form, 'edit_form':True})


@login_required
@render_to('profiles/manage_payments.html')
def manage_payments(request, redirect_url='profile_account'):
    objects = request.user.card_set.filter(deleted=False)
    form = CardForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        return HttpResponseRedirect(reverse('profile_account'))

    return {
        'form':form,
        'cards':objects,
    }


