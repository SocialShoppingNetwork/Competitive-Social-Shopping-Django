# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse


def test_checkout_shipping(logged_client, finished_auction):
    res = logged_client.get(reverse('checkout_shipping', kwargs={'auction_pk':
                 finished_auction.pk}))
    assert res.status_code == 200

def test_checkout_billing(logged_client, finished_auction, shipping_address):
    res = logged_client.get(reverse('checkout_billing', kwargs={
                                'auction_pk':finished_auction.pk,
                                'shipping_pk':shipping_address.pk}))
    assert res.status_code == 200

def test_checkout_payment(logged_client, finished_auction, shipping_address, billing_address):
    res = logged_client.get(reverse('checkout_payment', kwargs={
                                'auction_pk':finished_auction.pk,
                                'shipping_pk':shipping_address.pk,
                                'billing_pk':billing_address.pk
                            }))
    assert res.status_code == 200


def test_checkout_confirm_order(logged_client, finished_auction, shipping_address, billing_address, card):
    url = reverse('checkout_confirm_order', kwargs={
                            'auction_pk':finished_auction.pk,
                            'shipping_pk':shipping_address.pk,
                            'billing_pk':billing_address.pk,
                            'card_pk':card.pk
                            })
    res = logged_client.get(url)
    assert res.status_code == 200

    from checkout.models import Order
    from shipping.models import ShippingRequest
    ship_num = ShippingRequest.objects.count()
    order_num = Order.objects.count()
    res = logged_client.post(url)
    assert res.status_code == 302
    assert order_num + 1 ==  Order.objects.count()
    assert ship_num + 1 == ShippingRequest.objects.count()

