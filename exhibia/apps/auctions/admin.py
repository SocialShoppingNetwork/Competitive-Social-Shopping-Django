from django.contrib.admin import site
from django.contrib import admin
from auctions.models import Auction, AuctionItem, AuctionBid, AuctionItemImages, Category, Brand, AuctionPlegde

class AuctionItemAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    prepopulated_fields = {"slug_name": ("name",)}

site.register(Auction)
site.register(AuctionItem, AuctionItemAdmin)
site.register(AuctionItemImages)
site.register(AuctionBid)
site.register(AuctionPlegde)
site.register(Brand)
site.register(Category)


