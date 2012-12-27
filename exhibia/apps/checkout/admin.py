# -*- coding: utf-8 -*-
from checkout.models import Order
from django.contrib.admin import site
from django.contrib import admin

class OrderAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'user', 'tracking_number', 'created')
    list_filter = ('created', )
    date_hierarchy = 'created'
    raw_id_fields = ('auction', 'card', 'user', )

    fieldsets = (
        (None, {
            'fields': ('user', 'auction', 'card', 'tracking_number', 'shipping_company','status', )
        }),
        ('Shipping address', {
            'fields': ('shipping_first_name', 'shipping_last_name', 'shipping_address1',
                       'shipping_address2', 'shipping_city', 'shipping_state',
                       'shipping_country', 'shipping_zip_code', 'shipping_phone')
        }),
        ('Billing address', {
            'fields': ('billing_first_name', 'billing_last_name', 'billing_address1',
                       'billing_address2', 'billing_city', 'billing_state',
                       'billing_country', 'billing_zip_code', 'billing_phone')
        }),
    )


    def item_name(self, obj):
        return obj.auction.item.name

site.register(Order, OrderAdmin)
