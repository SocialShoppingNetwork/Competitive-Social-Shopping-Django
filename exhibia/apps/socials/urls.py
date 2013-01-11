from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("socials.views",
    url(r"^reward/like/item/$", "reward_like_item", name="reward_like_item"),
    url(r"^add_invitation/$",'add_invitation', name='add_invitation')
)
