from shipping.models import ShippingFee
from django.contrib.admin import site
from django.contrib import admin

class ShippingFeeAdmin(admin.ModelAdmin):
    raw_id_fields = ('item',)
    search_fields = ('item',)


site.register(ShippingFee, ShippingFeeAdmin)
