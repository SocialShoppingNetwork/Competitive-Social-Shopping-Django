# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import StoreItem


@login_required
def store_list(request):
    return render(request, 'points_store/storeitem_list.html',
                  {'active_items': StoreItem.objects.filter(active=True)})
