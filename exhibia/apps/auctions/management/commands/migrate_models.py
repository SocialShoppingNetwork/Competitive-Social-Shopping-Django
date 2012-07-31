from django.core.management.base import BaseCommand
from django.core.cache import cache
from time import sleep, time

from auctions.models import AuctionItem, AuctionItemImages
from bidin.models import AuctionItem as OldAuctionItem
from bidin.models import AuctionItemImages as OldAuctionItemImages

import settings
import threading
import cjson

class Command(BaseCommand):
    def handle(self, **options):
        """
        for a in OldAuctionItem.objects.using('bt03').all():
            AuctionItem.objects.create(code=a.code,
                                       name=a.name,
                                       slug_name=a.name_slug,
                                       bidding_time=a.bidding_time,
                                       price=a.price,

                                       amount=a.amount,
                                       shipping_fee=a.shipping_fee,
                                       description=a.description)
        """
        for image in OldAuctionItemImages.objects.using('bt03').all():
            try:
                item = AuctionItem.objects.get(slug_name=image.item.name_slug)
                AuctionItemImages.objects.create(item=item,
                                                 img=image.img,
                                                 is_default=image.is_default)
            except Exception, e :
                pass



