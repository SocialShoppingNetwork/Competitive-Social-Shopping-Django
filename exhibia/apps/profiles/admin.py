# -*- coding: utf-8 -*-

import datetime

from django.contrib import admin
from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse
from django.db.models import Count, Sum
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from pinax.apps.account.models import Account, PasswordReset
from social_auth.db.django_models import UserSocialAuth

from payments.models import AuctionOrder
from profiles.models import Member, BillingAddress, BannedIPAddress, IPAddress
from profiles.forms import DateRangeForm


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
            url(r'^analytics/$', self.analytics_view, name='user_analytics'),
        ) + super(CustomUser, self).get_urls()

    def ban_user(self, request, user_pk):
        for ip in IPAddress.objects.filter(user__pk=int(user_pk)):
            BannedIPAddress.objects.get_or_create(IPAddress=ip.IPAddress)
        return redirect(reverse('admin:auth_user_changelist'))

    def analytics_view(self, request):
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=7)
        form = DateRangeForm(data=request.POST or None,
                                  initial={ 'end_date': end_date,
                                            'start_date': start_date})
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
        end_date = end_date+datetime.timedelta(1)
        providers = UserSocialAuth.objects.distinct('provider').values_list('provider', flat=True)
        rows = []
        socials_pks = []
        for provider in providers:
            social_users = User.objects.filter(social_auth__provider=provider,
                              date_joined__range=(start_date, end_date))
            orders = list(AuctionOrder.objects.filter(winner__pk__in=\
                       social_users.values_list('pk', flat=True).query))
            socials_pks.extend(i.pk for i in social_users)
            rows.append({'provider':provider,
                        'user_count': social_users.count(),
                        'sale_count': len(orders),
                        'sale_amount': sum(i.amount_paid for i in orders) or 0
            })
        plain_users = User.objects.filter(date_joined__range=(start_date, end_date))\
                    .exclude(pk__in=socials_pks)
        orders = list(AuctionOrder.objects.filter(winner__pk__in=\
                                plain_users.values_list('pk', flat=True).query))
        rows.append({
                    'provider':'Plain registration',
                    'user_count': plain_users.count(),
                    'sale_count': len(orders),
                    'sale_amount': sum(i.amount_paid for i in orders) or 0
                    })
        return render(request, 'admin/auth/user/analytics.html',
                      {'form':form,
                      'media': self.media,
                      'opts': self.opts,
                      'title' : "User analytics",
                      'rows':rows,
                      'total_users_joined': sum(i['user_count'] for i in rows),
                      'total_sale_amount': sum(i['sale_amount'] for i in rows),
                      'total_sale_count': sum(i['sale_count'] for i in rows)
        })


admin.site.register(BannedIPAddress, BannedIPAddressAdmin)

admin.site.unregister(User)
admin.site.register(User, CustomUser)
admin.site.unregister(Account)
admin.site.unregister(PasswordReset)
