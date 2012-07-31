from django.db import models
from django.db.models import F
from django.core.validators import RegexValidator
from auctions.exceptions import AlreadyHighestBid, AuctionExpired, AuctionIsNotReadyYet
from time import time
from random import randint


class AuctionItem(models.Model):
    code = models.CharField(max_length=15,
                            primary_key=True,
                            db_index=True,
                            validators=[RegexValidator('^[a-zA-Z0-9-]+$')],
                            help_text="""This field is used to identify p, make sure its value is UNIQUE,\
                            it is NOT allowed to modify after the first time you add it.\
                            Only letters, numbers or hyphens are valid""")
    price = models.FloatField()
    name = models.CharField(max_length=150)
    name_slug = models.SlugField(max_length=200, unique=True)
    #category = models.ForeignKey(Category, blank=True, null=True)
    cashback1 = models.PositiveSmallIntegerField(null=True, blank=True)
    cashback2 = models.PositiveSmallIntegerField(null=True, blank=True)
    bidding_time = models.PositiveSmallIntegerField(default=120)
    description = models.TextField()
    amount = models.PositiveSmallIntegerField("Amount left")
    shipping_fee = models.FloatField()
    notes = models.TextField(default="", null=True, blank=True)
    meta_title = models.CharField(max_length=300, blank=True, default="")
    meta_description = models.CharField(max_length=300, blank=True, default="")
    buyitnow = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.name

class AuctionItemImages(models.Model):
    item = models.ForeignKey(AuctionItem, related_name="images")
    img = models.ImageField(help_text="default image 120px height 200px width recommended", upload_to="items")
    is_default = models.BooleanField(default=False)