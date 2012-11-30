from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import get_list_or_404, get_object_or_404, render_to_response

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
from profiles.forms import BillingForm

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
@render_to('profiles/manage_shipping.html')
def manage_shipping(request):
    shipping_profiles = request.user.shipping_adddresses.filter(deleted=False)
    shipping = None
    id = request.GET.get('id')
    if 'delete' in request.GET:
        shipping = get_object_or_404(ShippingAddress, id=id, user=request.user)
        shipping.deleted = True
        shipping.save()
        return HttpResponseRedirect(reverse('account_shipping'))

    if request.method == 'POST':
        form = ShippingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if id:
                shipping = get_object_or_404(ShippingAddress, id=id, user=request.user)
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
                shipping.user = request.user
                shipping.save()
                return HttpResponseRedirect(reverse('account_shipping'))
    else:
        if id:
            shipping = get_object_or_404(ShippingAddress, id=id, user=request.user)
            form = ShippingForm(initial=shipping.__dict__)
        else:
            form = ShippingForm()

    return {
        'form':form,
        'shipping_profiles':shipping_profiles,
        'shipping':shipping
    }

@login_required
@render_to('profiles/manage_billing.html')
def manage_billing(request):
    billing_profiles = request.user.billing_addresses.filter(deleted=False)
    billing = None
    id = request.GET.get('id')
    if 'delete' in request.GET:
        billing = get_object_or_404(BillingAddress, id=id, user=request.user, deleted=False)
        billing.deleted = True
        billing.save()
        return HttpResponseRedirect(reverse('profile_account'))

    if request.method == 'POST':
        form = BillingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if id:
                billing = get_object_or_404(BillingForm, id=id, user=request.user,
                             deleted=False)
                billing.first_name =  data['first_name']
                billing.last_name = data['last_name']
                billing.address1 = data['address1']
                billing.address2 = data['address2']
                billing.city = data['city']
                billing.zip_code = data['zip_code']
                billing.country = data['country']
                billing.state = data['state']
                billing.phone = data['phone']
                billing.save()
            else:
                billing = form.save(commit=False)
                billing.user = request.user
                billing.save()
            return HttpResponseRedirect(reverse('profile_account'))
    else:
        if id:
            billing = get_object_or_404(BillingAddress, id=id, user=request.user,
                                     deleted=False)
            form = BillingForm(initial=billing.__dict__)
        else:
            form = BillingForm()

    return {
        'form':form,
        'billing_profiles':billing_profiles,
        'billing':billing
    }

@login_required
@render_to('profiles/manage_payments.html')
def manage_payments(request):
    member = request.user.get_profile()
    cards = member.card_set.filter(deleted=False)
    card = None
    id = request.GET.get('card')
    if 'delete' in request.GET:
        card = get_object_or_404(Card, id=id, member=member, deleted=False)
        card.deleted = True
        card.save()
        return HttpResponseRedirect(reverse('profile_account'))

    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if id:
                data = form.cleaned_data
                card = form.save(commit=False)
                card.member = member
                card.save()
                cards = member.card_set.filter(deleted=False)
                form = CardForm()

            return HttpResponseRedirect(reverse('profile_account'))
    else:
        if id:
            card = get_object_or_404(Card, id=id, member=member, deleted=False)
            form = CardForm(initial=billing.__dict__)
        else:
            form = CardForm()

    return {
        'form':form,
        'cards':cards,
        'card':card
    }

