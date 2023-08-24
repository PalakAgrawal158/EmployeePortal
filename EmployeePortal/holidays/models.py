from django.db import models

# Create your models here.

class Holidays(models.Model):
    holiday_name = models.CharField(max_length=50)
    date = models.DateField()
    day = models.CharField(max_length=20)



