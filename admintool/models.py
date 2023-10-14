from django.utils import timezone

from django.db import models



class Status (models.Model):
    class Meta:
        verbose_name_plural = "Status"
   

class DataStatus(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateTimeField(default=timezone.now)
    value = models.BigIntegerField(verbose_name="Count")
    
    class Meta:
        verbose_name_plural = "Data Status"
