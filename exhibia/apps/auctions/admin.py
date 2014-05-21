from django.contrib.admin import site
from django.contrib import admin
from auctions.models import Auction, AuctionItem, AuctionBid, AuctionItemImages, Category, Brand, AuctionPlegde


class AuctionItemImagesInline(admin.TabularInline):
    model = AuctionItemImages
    extra = 0
    # max_num = 0


class PrepAdmin(object):
   prepopulated_fields = {"slug": ("name",)}


class AuctionItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'amount', 'shipping_fee', 'categories_inline')
    list_filter = ('created', )
    date_hierarchy = 'created'
    search_fields = ('name',)
    # raw_id_fields = ('image',)
    exclude = ('pledge_time', 'showcase_time',)
    prepopulated_fields = {"slug_name": ("name",)}
    inlines = [AuctionItemImagesInline, ]

    def save_model(self, request, obj, form, change):
        created = obj.pk
        super(AuctionItemAdmin, self).save_model(request, obj, form, change)
        if not created:
            Auction.objects.create_from_item(obj)







class AutciotnBidAdmin(admin.ModelAdmin):
    list_display = ('auction', 'bidder', 'price')
    list_filter = ('created', )
    date_hierarchy = 'created'
    raw_id_fields = ('auction', 'bidder')


class AuctionPlegdeAdmin(admin.ModelAdmin):
    list_display = ('auction', 'member', 'amount', 'created')
    list_filter = ('created', )
    raw_id_fields = ('auction', 'member')
    date_hierarchy = 'created'


class AuctionAdmin(admin.ModelAdmin):
    list_display = ('item', 'status', 'backers', 'current_offer', )
    list_filter = ('status', 'created', )
    date_hierarchy = 'created'
    raw_id_fields = ('item', 'last_bidder_member', )


class CategoryAdmin(PrepAdmin, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class BrandADmin(PrepAdmin, admin.ModelAdmin):
    pass


site.register(Auction, AuctionAdmin)
site.register(AuctionItem, AuctionItemAdmin)
site.register(AuctionBid, AutciotnBidAdmin)
site.register(AuctionPlegde, AuctionPlegdeAdmin)
site.register(Brand)
site.register(Category)


