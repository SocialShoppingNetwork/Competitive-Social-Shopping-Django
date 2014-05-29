import settings
from django import template
from payments.views import create_gateway

register = template.Library()


@register.inclusion_tag('auctions/auction_bid_button.html',  takes_context=True)
def bid_button(context, auction):
    """
    In this template tag we should decide should we add bid button or not
    """
    user = context['user']
    params = {'auction_id': auction.id, 'bid_allowed': False}
    if user.is_authenticated():
        profile = user.get_profile()
        if profile.is_on_win_limit:

            return params
        if auction.item.newbie:
            if profile.is_newbie or not user.is_authenticated():
                params['bid_allowed'] = True
                return params
            else:
                params['newbie'] = True
                return params

        else:
            params['bid_allowed'] = True
            return params
    else:
        params['bid_allowed'] = True
        return params