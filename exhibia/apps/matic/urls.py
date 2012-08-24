from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
    url(r"^index/$", "matic.views.admin_index", name="matic_admin"),
    url(r"^status/$", "matic.views.auctions_status", name="matic_status"),
    url(r"^change/status/(\d+)/$", "matic.views.pause_resume", name="matic_change_status"),
    url(r"^change/time/(\d+)/(\d+)/$", "matic.views.change_bidding_time", name="matic_change_bidding_time"),
    url(r"^pause/all/$", "matic.views.pause_all", name="matic_pause_all"),
    url(r"^resume/all/$", "matic.views.resume_all", name="matic_resume_all"),
)
