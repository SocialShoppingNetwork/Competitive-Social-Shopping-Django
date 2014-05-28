# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response, redirect, render

from annoying.decorators import render_to
from social_auth.backends import get_backends

from auctions.models import Auction
from shipping.forms import MemberInfoFormUS
from payments.constants import *
from payments.forms import CardForm
from payments.models import Card
from shipping.models import ShippingAddress
from profiles.forms import DeleteForm

from django.views.generic import CreateView
from braces.views import LoginRequiredMixin, SetHeadlineMixin


class AddressView(LoginRequiredMixin, SetHeadlineMixin, CreateView):
    headline = "Select your shipping address"
    model = ShippingAddress
    template_name = 'profiles/manage_address.html'
    form_class = MemberInfoFormUS
    choose_address = False

    def get_context_data(self, **kwargs):
        ctx = super(AddressView, self).get_context_data(**kwargs)
        ctx['kwargs'] = self.kwargs
        ctx['choose_address'] = self.choose_address
        ctx['objects'] = self.model.objects.filter(deleted=False, user=self.request.user)
        return ctx

    def form_valid(self, form):
        instance = form.save(False)
        instance.user = self.request.user
        instance.save()
        return redirect(self.request.path)


class CardCreateView(LoginRequiredMixin, SetHeadlineMixin, CreateView):
    model = Card
    headline = "Manage your plastic cards"
    template_name = "profiles/manage_payments.html"
    form_class = CardForm
    choose_card = False

    def get_context_data(self, *args, **kwargs):
        ctx = super(CardCreateView, self).get_context_data(*args, **kwargs)
        ctx['cards'] = self.model.objects.filter(deleted=False, user=self.request.user)
        ctx['kwargs'] = self.kwargs
        ctx['choose_card'] = self.choose_card
        return ctx

    def form_valid(self, form):
        instance = form.save(False)
        instance.user = self.request.user
        instance.save()
        return redirect(self.request.path)


@login_required
def auctions_won(request, template_name='profiles/auctions_won.html'):
    member = request.member
    auctionorders_unpaid = AuctionOrder.objects.filter(status=ORDER_NOT_PAID, winner=request.user)
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
    auction = get_object_or_404(Auction, id=auction_id, last_bidder=request.user.username, status="f")
    if request.POST:
        confirm = request.POST.get('confirm', 'no')
        if confirm == "yes":
            order = AuctionOrder.objects.create_order(auction, request.user)
            return HttpResponseRedirect('/accounts/profile/won/')
    c = RequestContext(request, {"a": auction,
                                 "member": member,
                                 'shipping': request.user.shipping_addresses.all()[0], })
    return render_to_response(template_name, context_instance=c)


@login_required
def order_pay(request, order_id):
    print order_id
    # import pdb
    # pdb.set_trace()
    order = get_object_or_404(AuctionOrder, id=order_id, winner=request.user, auction__status="m")
    return render(request, 'order_pay.html', {
        "order": order,
        "dalpay_form": None,
        # "dalpay_form": auction_form(request, 'dalpay', order_id),
    }
    )


def member_bids(request):
    """ returns the number of bid of the current user """
    if not request.user.is_authenticated():
        return HttpResponse("0")
    return HttpResponse(str(request.member.credits))


ORDER_WAITING_PAYMENT = 'wp'
ORDER_SHIPPING_FEE_REQUESTED = 'rf'
ORDER_PROCESSING_ORDER = 'op'
ORDER_PAID = 'pd'  # Processing Order
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
    auctions_waiting_payment = request.user.items_won.all()  # .filter(order=None)

    #orders processing and shipped
    auctions_processing = request.user.items_won.filter(order__status=ORDER_PROCESSING)

    # TODO we should show buy now auctions



    auctions_shipped = request.user.items_won.filter(order__status=ORDER_SHIPPED)
    available = set(get_backends().keys())
    associated = list(request.user.social_auth.all())
    not_associated = available.difference(i.provider for i in associated)
    print request.session.keys()
    return {'member': member,
            'auctions_waiting_payment': auctions_waiting_payment,
            'auctions_processing': auctions_processing,
            'auctions_shipped': auctions_shipped,
            'not_associated': not_associated,
            'associated': [i.provider for i in associated],
            'available_auth_backends': available,
    }


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
        except:
            pass
    return redirect(reverse(redirect_url))


@login_required
def manage_edit(request, pk, model=ShippingAddress, form=MemberInfoFormUS,
                redirect_url='account_shipping', template='profiles/manage_shipping.html'):
    obj = get_object_or_404(model, pk=pk)
    form = form(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect(redirect_url)
    return render(request, template,
                  {'form': form, 'edit_form': True})


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
        'form': form,
        'cards': objects,
    }


