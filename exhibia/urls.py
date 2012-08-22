from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

from pinax.apps.account.openid_consumer import PinaxConsumer


handler500 = "pinax.views.server_error"


urlpatterns = patterns("",
    #url(r"^$", direct_to_template, {
    #    "template": "homepage.html",
    #}, name="home"),
    url(r"^$", "auctions.views.index", name="home"),

    url(r"^bid/ajax/(\d+)/$", "auctions.views.bid_ajax", name="auction_bid_ajax"),
    #url(r"^bid/(\d+)/$", "auctions.views.bid", name="auction-item"),
    url(r"^bid/(\d+)/$", "auctions.views.auction_bid", name="auction_bid"),

    url(r'^item/(?P<slug>\S+).html$', 'auctions.views.view_item', {}, name='auction_item'),

    url(r"^buycredits/$", "payments.views.buycredits", name="buycredits"),

    url(r'^pay/package/dalpay/$', 'payments.views.package_order_dalpay', {}, name='package_order_dalpay'),
    url(r'^pay/auction/dalpay/$', 'payments.views.auction_order_dalpay', {}, name='auction_order_dalpay'),
    #url(r"^buycredits/$", "payments.views.auction_won", name="auction_won"),

    #url(r'^auction_winners/$', 'bidin.views.auction_winners', {}, name='auction_winners'),

    url(r'^accounts/profile/won/$', 'profiles.views.auctions_won', {}, name="auctions_won"),
    url(r'^accounts/profile/won/(?P<auction_id>\d+).html$', 'profiles.views.auction_won', {}, name='auction_won'),
    url(r'^accounts/profile/pay/(?P<order_id>\d+).html$', 'profiles.views.order_pay', {}, name="order_pay"),
    url(r'^accounts/profile/info/$', 'profiles.views.member_info', {}, name='member_info'),
    url(r'^accounts/profile/bids/$', 'profiles.views.member_bids', {}, name='member_bids'),
    url(r'^accounts/profile/bids/$', 'profiles.views.member_bids', {}, name='member_bids'),
    url(r'^accounts/profile/$', 'profiles.views.account', {}, name="profile_account"),

    url(r'^account/$', 'profiles.views.account', {}, name="profile_account"),

    url(r'^accounts/shipping/$', 'profiles.views.manage_shipping', {}, name="account_shipping"),

    
    url(r"^items/", include("auctions.urls")),

    #url(r"^testimonials/", include("testimonials.urls")),
    url(r"^matic/", include("matic.urls")),

    #u url(r'', include('social_auth.urls')),
    #u url(r'', include('social_login.urls')),

    url(r"^testimonials/", include("testimonials.urls")),
    url(r"^checkout/", include("checkout.urls")),


    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^about/", include("about.urls")),


    url(r"^account/", include("pinax.apps.account.urls")),
    url(r"^openid/", include(PinaxConsumer().urls)),
    url(r"^profiles/", include("idios.urls")),
    url(r"^notices/", include("notification.urls")),
    url(r"^announcements/", include("announcements.urls")),
    #url(r'^uploadify/', include('uploadify.urls')),
    url(r'^uploader/', include('uploader.urls')),
    url(r'^socials/', include('socials.urls')),
    url(r'^chat/', include('chat.urls')),
    (r'^tinymce/', include('tinymce.urls')),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'},  name='logout'),
    url(r'', include('social_auth.urls')),
)


if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
    )
