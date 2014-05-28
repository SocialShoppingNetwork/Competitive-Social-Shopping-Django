import datetime
import settings
from django import template
from django.core.urlresolvers import reverse

from annoying.functions import get_object_or_None
from socials.models import LikeItem
register = template.Library()
@register.inclusion_tag('payments/credits_checkout.html',  takes_context=True)
def credits_checkout(context):
    from payments.views import create_gateway
    user = context['user']
    gateway = create_gateway('dalpay',
                             custom1=user.username,
                             function='credits')
    try:
        member = user.get_profile()
    except:
        member = None
    print 'Meeeeember %s' % member
    params = {'gateway': gateway, 'member':member}
    return params