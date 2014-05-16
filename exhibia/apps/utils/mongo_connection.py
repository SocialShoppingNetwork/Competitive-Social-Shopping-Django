import pymongo
from django.conf import settings


def get_mongodb():
    """
    Enable connection to Mongo and return database "exhibia"
    @return: db: exhibia
    """
    mongo_client = pymongo.MongoClient(settings.MONGO['host'], settings.MONGO['port'])
    db = mongo_client.exhibia
    return db