from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
    url(r"^reward/like/item/$", "socials.views.reward_like_item", name="reward_like_item"),

)
