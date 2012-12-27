import datetime
import cjson

from django.http import Http404, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.views.decorators.csrf import csrf_exempt
from annoying.functions import get_object_or_None
from annoying.decorators import render_to

from auctions.models import Auction
from checkout.models import Order
from shipping.models import ShippingAddress, ShippingRequest
from shipping.forms import ShippingForm, get_shipping_form

from payments.models import Card
from payments.forms import CardForm

from profiles.forms import BillingForm
from profiles.models import BillingAddress


@login_required
def view_order(request, order_pk):
    return render(request, 'checkout/view_order.html',
                  {'order':get_object_or_404(Order, user=request.user, pk=order_pk)})

@login_required
def confirm_order(request, auction_pk, shipping_pk, billing_pk, card_pk):
    auction = get_object_or_404(request.user.items_won, pk=auction_pk)
    card = get_object_or_404(Card, user=request.user, pk=card_pk)
    shipping = get_object_or_404(ShippingAddress, user=request.user, pk=shipping_pk)
    billing = get_object_or_404(BillingAddress, user=request.user, pk=billing_pk)
    if request.method == "POST":
        # created shipping request so admin can review it and set a fee
        ShippingRequest.objects.create(
            auction=auction,
            user=request.user,
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
        # order itself
        Order.objects.create(
            auction=auction,
            card=card,
            user=request.user,

            shipping_first_name=shipping.first_name,
            shipping_last_name=shipping.last_name,
            shipping_address1=shipping.address1,
            shipping_address2=shipping.address2,
            shipping_city=shipping.city,
            shipping_country=shipping.country,
            shipping_zip_code=shipping.zip_code,
            shipping_phone=shipping.phone,
            shipping_state=shipping.state,

            billing_first_name=billing.first_name,
            billing_last_name=billing.last_name,
            billing_address1=billing.address1,
            billing_address2=billing.address2,
            billing_city=billing.city,
            billing_country=billing.country,
            billing_zip_code=billing.zip_code,
            billing_phone=billing.phone,
            billing_state=billing.state,
        )
        return redirect(reverse('profile_account'))
    return render(request, 'checkout/order_review.html',
                  {'auction':auction,
                  'card':card,
                  'shipping':shipping,
                  'billing':billing})



# TODO: remove rest of code as its not used anymore


@login_required
@render_to('checkout/select_shipping_address.html')
def select_shipping_address(request, auction_id):
    auction = get_object_or_404(request.user.items_won.filter(order=None), id=auction_id)
    shipping_profiles = request.user.shipping_adddresses.filter(deleted=False)
    next_url = request.REQUEST.get('next')

    id = request.POST.get('id')
    action = request.POST.get('action')
    shipping = None
    if id:
        shipping = get_object_or_404(ShippingAddress, id=id, user=request.user, deleted=False)
    session_shipping = 'auction_%s_shipping' % auction_id

    if 'delete' in request.POST:
        shipping.deleted = True
        shipping.save()
        return HttpResponseRedirect(reverse('checkout_select_shipping_address', args=[auction_id]))

    if 'select' in request.POST:
        request.session[session_shipping] = shipping.id
        if auction.item.shippingfee_set.filter(country=shipping.country).exists():
            redirect_url = reverse('checkout_select_shipping', args=[auction_id])
            if next_url:
                redirect_url = '%s?next=%s' % (redirect_url, next_url)
            return HttpResponseRedirect(redirect_url)
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
                    shipping.user = request.user
                    shipping.save()
                    request.session[session_shipping] = shipping.id
                    return HttpResponseRedirect(reverse('checkout_select_shipping_address', args=[auction_id]))
    else:
        form = ShippingForm()

    return {
        'next_url':next_url,
        'auction':auction,
        'form':form,
        'shipping_profiles':shipping_profiles,
        'shipping':shipping
    }

@login_required
@render_to('checkout/select_payment.html')
def select_payment(request, auction_id):
    session_card = 'auction_%s_payment' % auction_id
    # session_shipping = 'auction_%s_shipping' % auction_id

    member = request.user.get_profile()
    auction = get_object_or_404(request.user.items_won.filter(order=None), id=auction_id)
    cards = request.user.card_set.filter(deleted=False)

    id = request.POST.get('card')
    # action = request.POST.get('action')
    card = None
    if 'select' in request.POST:
        card = get_object_or_404(Card, id=id, user=request.user, deleted=False)
        request.session[session_card] = card.id
        return HttpResponseRedirect(reverse('checkout_review', args=[auction.id]))

    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            # data = form.cleaned_data
            card = form.save(commit=False)
            card.use = request.user
            card.save()
            request.session[session_card] = card.id
            cards = request.user.card_set.filter(deleted=False)
            form = CardForm()
    else:
        form = CardForm()

    return {
        'auction':auction,
        'form':form,
        'cards':cards,
        'card':card
    }



# @login_required
# @render_to('checkout/order_review.html')
# def review_order(request, auction_id):
#     session_card = 'auction_%s_payment' % auction_id
#     session_shipping = 'auction_%s_shipping' % auction_id
#     session_billing = 'auction_%s_billing' % auction_id
#     session_shipping_option = 'auction_%s_shipping_option' % auction_id

#     member = request.user.get_profile()
#     card_id = request.session.get(session_card)
#     shipping_id = request.session.get(session_shipping)
#     billing_id = request.session.get(session_billing)
#     shipping_option_id = request.session.get(session_shipping_option)

#     auction = get_object_or_404(request.user.items_won.filter(order=None), id=auction_id)
#     try:
#         order = auction.order
#         return HttpResponseRedirect(reverse('profile_account'))
#     except :
#         order = None
#     card = get_object_or_404(request.user.card_set.filter(deleted=False), id=card_id)
#     shipping = get_object_or_404(ShippingAddress, id=shipping_id, user=request.user, deleted=False)
#     # shipping_option = get_object_or_404(auction.item.shippingfee_set.all(), id=shipping_option_id)
#     #TODO verify country here

#     if billing_id:
#         billing = get_object_or_404(request.user.billingaddress_set.filter(deleted=False), id=billing_id)
#     else:
#         billing = BillingAddress.objects.filter(user=request.user)[0]

#     if request.POST:
#         Order.objects.create(
#             auction=auction,
#             card=card,
#             shipping_first_name=shipping.first_name,
#             shipping_last_name=shipping.last_name,
#             shipping_address1=shipping.address1,
#             shipping_address2=shipping.address2,
#             shipping_city=shipping.city,
#             shipping_country=shipping.country,
#             shipping_zip_code=shipping.zip_code,
#             shipping_phone=shipping.phone,
#             shipping_state=shipping.state,

#             billing_first_name=billing.first_name,
#             billing_last_name=billing.last_name,
#             billing_address1=billing.address1,
#             billing_address2=billing.address2,
#             billing_city=billing.city,
#             billing_country=billing.country,
#             billing_zip_code=billing.zip_code,
#             billing_phone=billing.phone,
#             billing_state=billing.state,
#             member=member
#         )

#         return HttpResponseRedirect(reverse('profile_account'))
#     return {
#         'card':card,
#         'shipping':shipping,
#         'billing':billing,
#         'auction':auction,
#         # 'shipping_option':shipping_option
#     }

@login_required
@render_to('checkout/request_shipping.html')
def request_shipping_fee(request, auction_id):
    session_shipping = 'auction_%s_shipping' % auction_id
    shipping_id = request.session.get(session_shipping)
    auction = get_object_or_404(request.user.items_won.filter(order=None), id=auction_id)
    shipping = get_object_or_None(ShippingAddress, id=shipping_id, user=request.user, deleted=False)

    try:
        if auction.order:
            raise HttpResponseBadRequest() # OR REDIRECT
    except Order.DoesNotExist:
        pass

    shipping_request = None
    try:
        shipping_request = auction.shippingrequest
    except ShippingRequest.DoesNotExist:
        if not shipping:
            return HttpResponseRedirect(reverse('checkout_select_shipping_address', args=[auction.id]))
            #Redirect

    if request.method == 'POST':
        if shipping_request:
            shipping_request.delete()
        shipping_request = ShippingRequest.objects.create(
            auction=auction,
            user=request.user,
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
    next_url = request.REQUEST.get('next')
    session_card = 'auction_%s_payment' % auction_id
    session_shipping = 'auction_%s_shipping' % auction_id
    session_shipping_option = 'auction_%s_shipping_option' % auction_id

    shipping_id = request.session.get(session_shipping)
    auction = get_object_or_404(request.user.items_won.filter(order=None), id=auction_id)
    shipping = get_object_or_404(ShippingAddress, id=shipping_id, user=request.user, deleted=False)
    if not auction.item.shippingfee_set.filter(country=shipping.country).exists():
        return HttpResponseRedirect(reverse('checkout_request_fee', args=[auction.id]))
    shipping_options = auction.item.shippingfee_set.all()
    if request.method == 'POST':
        shipping_id = request.POST.get('shipping')
        shipping_option = get_object_or_404(auction.item.shippingfee_set.all(), id=shipping_id)
        request.session[session_shipping_option] = shipping_option.id

        if next_url:
            redirect_url = next_url
        else:
            redirect_url = reverse('checkout_select_payment', args=[auction_id])
        return HttpResponseRedirect(redirect_url)
    return {
        'next_url':next_url,
        'auction':auction,
        'shipping_options':shipping_options,
        'shipping':shipping,
    }

@login_required
@render_to('checkout/select_billing_address.html')
def select_billing(request, auction_id):
    member = request.user.get_profile()
    auction = get_object_or_404(member.items_won.filter(order=None), id=auction_id)
    billing_profiles = member.billingaddress_set.filter(deleted=False)
    next_url = request.REQUEST.get('next')

    id = request.POST.get('id')
    action = request.POST.get('action')
    billing = None
    if id:
        billing = get_object_or_404(BillingAddress, id=id, member=member, deleted=False)
    session_billing = 'auction_%s_billing' % auction_id

    if 'delete' in request.POST:
        billing.deleted = True
        billing.save()
        return HttpResponseRedirect(reverse('checkout_select_billing_address', args=[auction_id]))

    if 'select' in request.POST:
        request.session[session_billing] = billing.id
        return HttpResponseRedirect(reverse('checkout_review', args=[auction.id]))

    if request.method == 'POST':
        if action =='edit':
            form = BillingForm(initial=billing.__dict__)
        else:
            form = BillingForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                if billing:
                    #Update and Select
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
                    request.session[session_billing] = billing.id
                    return HttpResponseRedirect(reverse('checkout_select_billing_address', args=[auction_id]))
                else:
                    #Create new Billing address, SAVE
                    billing = form.save(commit=False)
                    billing.member = member
                    billing.save()
                    request.session[session_billing] = billing.id
                    return HttpResponseRedirect(reverse('checkout_select_billing_address', args=[auction_id]))
    else:
        form = BillingForm()

    return {
        'next_url':next_url,
        'auction':auction,
        'form':form,
        'billing_profiles':billing_profiles,
        'billing':billing,
    }

# @login_required
# @render_to('checkout/view_order.html')
# def view_order(request, order_id):
#     member = request.user.get_profile()
#     order = get_object_or_404(member.order_set.all(), id=order_id)
#     return {
#         'order':order,
#     }
