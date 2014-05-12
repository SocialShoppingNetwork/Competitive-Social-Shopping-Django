from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
    url(r"^get/$", "auctions.views.get_auctions", name="auction_get"),
    url(r"^(?P<auction_id>\d+)/$", "auctions.views.auction_info", name="auction_info"),
    url(r"^info/$", "auctions.views.auctions_info", name="auctions_info"),

    url(r"^fund/(?P<auction_id>\d+)/", "auctions.views.fund", name="auction_fund"),
    url(r"^pledge/(\d+)/$", "auctions.views.pledge", name="auction_pledge"),
    url(r"^checkout/$", "auctions.views.checkout", name='auctions_checkout'),
    url(r"^append-funding-carousel/$", "auctions.views.append_funding_carousel", name="append_funding_carousel"),
)