from django.db import models


class Matches(models.Model):
    mid = models.IntegerField(max_length=500)
    name = models.CharField(max_length=500, null=True)
    address = models.CharField(max_length=500, null=True)
    url = models.CharField(max_length=500, null=True)
    coordinates = models.CharField(max_length=500, null=True)
    matches = models.CharField(max_length=2000, null=True)
    phone = models.CharField(max_length=500, null=True)

    def __unicode__(self):
        return "%s: %s"%(self.mid, self.name)

class Irrelevant(models.Model):
    IrrelevantID = models.IntegerField(max_length=500)

    def __unicode__(self):
        return self.IrrelevantID

class MatchedID(models.Model):
    MatchID = models.IntegerField(max_length=500)

class ConfirmedMatched(models.Model):
    mid = models.IntegerField(max_length=500)
    hid = models.IntegerField(max_length=500)

    def __unicode__(self):
        return "Hotel ID: %s, Matched Hotel ID %s"%(self.mid, self.hid)