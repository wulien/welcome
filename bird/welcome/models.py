from django.db import models

# Create your models here.
class WaitForVerify(models.Model):
    ip = models.IPAddressField()
    phone_no = models.CharField(max_length=13)
    random_no = models.SmallIntegerField()
    time = models.DateTimeField(auto_now_add=True)
    reserve = models.CharField(max_length=32)

    def __unicode__(self):
        return self.phone_no

class OnLine(models.Model):
    ip = models.IPAddressField()
    phone_no = models.CharField(max_length=16)
    time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.phone_no

class HistoryInfo(models.Model):
    phone_no = models.CharField(max_length=16)
    time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.phone_no

