# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import StoreItem, BoughtItem


class StoreItemAdmin(admin.ModelAdmin):
    list_display = ('item_type', 'cost', 'duration', 'active')
    list_filter = ('item_type', 'active')

class BoughtItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'bought_at')
    list_filter = ('bought_at', )
    raw_id_fields = ('user', )
    date_hierarchy = 'bought_at'
admin.site.register(StoreItem, StoreItemAdmin)
admin.site.register(BoughtItem, BoughtItemAdmin)
