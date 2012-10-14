# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from .models import ReferralLink

def refferal(request, ref_id):
    try:
        ref = ReferralLink.objects.get(pk=int(ref_id))
    except Exception:
        return redirect(reverse('home'))
    if ref.is_blocked:
        return redirect(reverse('home'))
    request.session['referral_link'] = ref.pk
    ref.visit_count += 1
    ref.save()
    return redirect(ref.redirect_to)
