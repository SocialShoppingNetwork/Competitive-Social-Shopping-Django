# -*- coding: utf-8 -*-

from django.contrib import admin

from referrals.models import ReferralLink


class ReferralLinkAdmin(admin.ModelAdmin):
    list_display = ('user', 'redirect_to', 'visit_count', 'is_blocked')
    list_filter = ('is_blocked', )



admin.site.register(ReferralLink, ReferralLinkAdmin)
