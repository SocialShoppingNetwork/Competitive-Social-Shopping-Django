import datetime
from django.db import models
class LikeItem(models.Model):
    LIKE_TYPES = (
        ("F", "Facebook"),
        ("G", "Google Plus"),
        ("Y", "Youtube")
    )
    item = models.ForeignKey('auctions.AuctionItem')
    member = models.ForeignKey('profiles.Member')
    type = models.CharField(choices=LIKE_TYPES, max_length=1)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("item", "member", "type")
