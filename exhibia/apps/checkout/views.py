import datetime
import cjson

from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, get_object_or_404, render_to_response
from django.core.cache import cache
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseGone
from annoying.functions import get_object_or_None
from annoying.decorators import render_to, ajax_request

from auctions.models import Auction
from checkout.models import Order
from shipping.models import ShippingAddress, ShippingRequest
from shipping.forms import ShippingForm

@login_required
@render_to('checkout/select_shipping_address.html')
def select_shipping_address(request, auction_id):
    member = request.user.get_profile()
    auction = get_object_or_404(member.items_won.filter(order=None), id=auction_id)
    shipping_profiles = member.shippingaddress_set.filter(deleted=False)

    id = request.POST.get('id')
    action = request.POST.get('action')
    shipping = None
    if id:
        shipping = get_object_or_404(ShippingAddress, id=id, member=member, deleted=False)
    session_shipping = 'auction_%s_shipping' % auction_id

    if 'delete' in request.POST:
        shipping.deleted = True
        shipping.save()
        return HttpResponseRedirect(reverse('checkout_select_shipping_address', args=[auction_id]))

    if 'select' in request.POST:
        request.session[session_shipping] = shipping.id
        if auction.item.shippingfee_set.filter(country=shipping.country).exists():
            return HttpResponseRedirect(reverse('checkout_select_shipping', args=[auction_id]))
        else:
            return HttpResponseRedirect(reverse('checkout_request_fee', args=[auction_id]))

    if request.method == 'POST':
        if action =='edit':
            form = ShippingForm(initial=shipping.__dict__)
        else:
            form = ShippingForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                if shipping:
                    #Update and Select
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
                    request.session[session_shipping] = shipping.id
                    return HttpResponseRedirect(reverse('checkout_select_shipping_address', args=[auction_id]))
                else:
                    #Create new Shipping address, SAVE
                    shipping = form.save(commit=False)
                    shipping.member = member
                    shipping.save()
                    request.session[session_shipping] = shipping.id
                    return HttpResponseRedirect(reverse('checkout_select_shipping_address', args=[auction_id]))
    else:
        form = ShippingForm()

    return {
        'auction':auction,
        'form':form,
        'shipping_profiles':shipping_profiles,
        'shipping':shipping
    }

from payments.models import Card
from payments.forms import CardForm

@login_required
@render_to('checkout/select_payment.html')
def select_payment(request, auction_id):
    session_card = 'auction_%s_payment' % auction_id
    session_shipping = 'auction_%s_shipping' % auction_id

    member = request.user.get_profile()
    auction = get_object_or_404(member.items_won.filter(order=None), id=auction_id)
    cards = member.card_set.filter(deleted=False)

    id = request.POST.get('card')
    action = request.POST.get('action')
    card = None
    if 'select' in request.POST:
        card = get_object_or_404(Card, id=id, member=member, deleted=False)
        request.session[session_card] = card.id
        return HttpResponseRedirect(reverse('checkout_review', args=[auction.id]))

    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            card = form.save(commit=False)
            card.member = member
            card.save()
            request.session[session_card] = card.id
            cards = member.card_set.filter(deleted=False)
            form = CardForm()
    else:
        form = CardForm()

    return {
        'auction':auction,
        'form':form,
        'cards':cards,
        'card':card
    }

@login_required
@render_to('checkout/order_review.html')
def review_order(request, auction_id):
    session_card = 'auction_%s_payment' % auction_id
    session_shipping = 'auction_%s_shipping' % auction_id
    session_billing = 'auction_%s_billing' % auction_id
    session_shipping_option = 'auction_%s_shipping_option' % auction_id

    member = request.user.get_profile()
    card_id = request.session.get(session_card)
    shipping_id = request.session.get(session_shipping)
    billing_id = request.session.get(session_billing)
    shipping_option_id = request.session.get(session_shipping_option)

    auction = get_object_or_404(member.items_won.filter(order=None), id=auction_id)
    card = get_object_or_404(member.card_set.filter(deleted=False), id=card_id)
    shipping = get_object_or_404(ShippingAddress, id=shipping_id, member=member, deleted=False)
    shipping_option = get_object_or_404(auction.item.shippingfee_set.all(), id=shipping_option_id)


    return {
        'card' : card,
        'shipping': shipping,
        'auction': auction,
        'shipping_option':shipping_option
    }

@login_required
@render_to('checkout/request_shipping.html')
def request_shipping_fee(request, auction_id):
    member = request.user.get_profile()
    session_shipping = 'auction_%s_shipping' % auction_id
    shipping_id = request.session.get(session_shipping)
    auction = get_object_or_404(member.items_won.filter(order=None), id=auction_id)
    shipping = get_object_or_None(ShippingAddress, id=shipping_id, member=member, deleted=False)

    try:
        if auction.order:
            raise HttpResponseBadRequest() # OR REDIRECT
    except Order.DoesNotExist:
        pass
    try:
        shipping_request = auction.shippingrequest
    except ShippingRequest.DoesNotExist:
        if not shipping:
            return HttpResponseRedirect(reverse('checkout_select_shipping_address', args=[auction.id]))
            #Redirect
        shipping_request = None

    if request.method == 'POST':
        if shipping_request:
            shipping_request.delete()
        shipping_request = ShippingRequest.objects.create(
            auction=auction,
            member=member,
            first_name=shipping.first_name,
            last_name=shipping.last_name,
            address1=shipping.address1,
            address2=shipping.address2,
            city=shipping.city,
            state=shipping.state,
            country=shipping.country,
            zip_code=shipping.zip_code,
            phone=shipping.phone,
        )
    return {
        'auction':auction,
        'shipping':shipping,
        'shipping_request':shipping_request,
    }

@login_required
@render_to('checkout/select_shipping.html')
def select_shipping(request, auction_id):
    member = request.user.get_profile()

    session_card = 'auction_%s_payment' % auction_id
    session_shipping = 'auction_%s_shipping' % auction_id
    session_shipping_option = 'auction_%s_shipping_option' % auction_id

    shipping_id = request.session.get(session_shipping)
    auction = get_object_or_404(member.items_won.filter(order=None), id=auction_id)
    shipping = get_object_or_404(ShippingAddress, id=shipping_id, member=member, deleted=False)
    if not auction.item.shippingfee_set.filter(country=shipping.country).exists():
        return HttpResponseRedirect(reverse('checkout_request_fee', args=[auction.id]))
    shipping_options = auction.item.shippingfee_set.all()
    if request.method == 'POST':
        shipping_id = request.POST.get('shipping')
        shipping_option = get_object_or_404(auction.item.shippingfee_set.all(), id=shipping_id)
        request.session[session_shipping_option] = shipping_option.id
        return HttpResponseRedirect(reverse('checkout_select_payment', args=[auction_id]))
    return {
        'auction':auction,
        'shipping_options':shipping_options,
        'shipping':shipping,
    }






