from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
    url(r"^admin/$", "matic.views.admin_index", name="matic_admin"),
    url(r"^status/$", "matic.views.auctions_status", name="matic_status"),
    url(r"^change/win/(\d+)/$", "matic.views.change_win", name="matic_change_win"),
    url(r"^change/status/(\d+)/$", "matic.views.pause_resume", name="matic_change_status"),
    url(r"^change/bidsleft/(\d+)/(\d+)/$", "matic.views.change_bids_left", name="matic_change_bids_left"),
    url(r"^change/time/(\d+)/(\d+)/$", "matic.views.change_bidding_time", name="matic_change_bidding_time"),
    url(r"^pause/all/$", "matic.views.pause_all", name="matic_pause_all"),
    url(r"^resume/all/$", "matic.views.resume_all", name="matic_resume_all"),
    url(r"^bid/(\d+)/$", "matic.views.bid", name="matic_bid"),
)
