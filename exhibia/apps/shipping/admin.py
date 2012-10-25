# -*- coding: utf-8 -*-

from django.contrib.admin import site
from django.contrib import admin

from shipping.models import ShippingFee, ShippingRequest


class ShippingRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'auction', 'waiting', 'created')
    list_filter = ('waiting', 'created', )
    date_hierarchy = 'created'
    raw_id_fields = ('user', 'auction', )


class ShippingFeeAdmin(admin.ModelAdmin):
    list_display = ('item', 'country', 'shipping', 'price')
    list_filter = ('shipping','created' ,'country', )
    raw_id_fields = ('item',)
    search_fields = ('item',)


site.register(ShippingRequest, ShippingRequestAdmin)
site.register(ShippingFee, ShippingFeeAdmin)
