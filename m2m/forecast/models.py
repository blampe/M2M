from django.db import models

# Create your models here.

class Forecast(models.Model):
   partner_id = models.CharField(max_length=30, unique=True)
   key = models.CharField(max_length=30)
   location_id = models.CharField(max_length=30)

