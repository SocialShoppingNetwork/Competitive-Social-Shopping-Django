from django.contrib.admin import site
from auctions.models import Auction, AuctionItem, AuctionBid, AuctionItemImages, Category, Brand

site.register(Auction)
site.register(AuctionItem)
site.register(AuctionItemImages)
site.register(AuctionBid)
site.register(Brand)
site.register(Category)
