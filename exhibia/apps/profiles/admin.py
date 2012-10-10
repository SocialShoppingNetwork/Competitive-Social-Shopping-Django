# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from profiles.models import Member, BillingAddress

class BillingAddressInline(admin.StackedInline):
    model = BillingAddress
    extra = 0
    max_num = 0

class ProfileInline(admin.StackedInline):
    model = Member
    max_num = 0
    extra = 0


admin.site.unregister(User)

class CustomUser(UserAdmin):
    inlines = UserAdmin.inlines+[ProfileInline, BillingAddressInline]


admin.site.register(User, CustomUser)
