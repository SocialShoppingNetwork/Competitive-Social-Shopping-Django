from django.contrib.sites.models import Site

def full_url(url):
    site = Site.objects.get_current()
    return ''.join(['http://', site.domain, url])


def auction_to_dict(auction):
    return {"id": auction.id,
            "status": auction.status,
            "last_bidder": auction.last_bidder,
            "time_left": auction.time_left,
            "current_offer": auction.current_offer,
            "bidding_time": auction.bidding_time,
            "backers": auction.backers,
            "amount_pleged": auction.amount_pleged,
            "time_to_go": auction.time_to_go,
            "funded": auction.funded}

def to_json(auction):
    return {"id": auction.id,
            "status": auction.status,
            "last_bidder": auction.last_bidder,
            "time_left": auction.time_left,
            "current_price": auction.current_offer,
            "bidding_time": auction.bidding_time}

def auctions_to_dict(auctions):
    result = {}
    for a in auctions:
        result['a_%s' % a.id] =  auction_to_dict(a)
    return result