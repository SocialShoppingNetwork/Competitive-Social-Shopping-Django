from django.db import models

class Message(models.Model):
    member = models.ForeignKey("profiles.Model")
    message = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.message

class BanList(models.Model):
    member = models.ForeignKey("profiles.Member")
    def __unicode__(self):
        return str(self.member)
