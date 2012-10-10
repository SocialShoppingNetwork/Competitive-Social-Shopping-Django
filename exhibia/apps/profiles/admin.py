# -*- coding: utf-8 -*-
from django.contrib import admin
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from pinax.apps.account.models import Account, PasswordReset
from profiles.models import Member, BillingAddress, BannedIPAddress, IPAddress

class BillingAddressInline(admin.StackedInline):
    model = BillingAddress
    extra = 0
    max_num = 0

class ProfileInline(admin.StackedInline):
    model = Member
    max_num = 0
    extra = 0

class IPAddressInline(admin.TabularInline):
    model = IPAddress
    max_num = 0
    extra = 0
    readonly_fields = ('last_login', 'IPAddress')

class BannedIPAddressAdmin(admin.ModelAdmin):
    model = BannedIPAddress


class CustomUser(UserAdmin):
    inlines = UserAdmin.inlines+[ProfileInline, BillingAddressInline, IPAddressInline]
    change_form_template = 'change_user.html'
    select_related = True
    def get_urls(self):
        from django.conf.urls.defaults import patterns, url
        return patterns('',
            url(r'^ban/(?P<user_pk>\d+)/$', self.ban_user, name='ban_user'),
        ) + super(CustomUser, self).get_urls()

    def ban_user(self, request, user_pk):
        for ip in IPAddress.objects.filter(user__pk=int(user_pk)):
            BannedIPAddress.objects.get_or_create(IPAddress=ip.IPAddress)
        return redirect(reverse('admin:auth_user_changelist'))


admin.site.register(BannedIPAddress, BannedIPAddressAdmin)

admin.site.unregister(User)
admin.site.register(User, CustomUser)
admin.site.unregister(Account)
admin.site.unregister(PasswordReset)
