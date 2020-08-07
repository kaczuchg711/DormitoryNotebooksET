from django.db import models


# Create your models here.

class Organization(models.Model):
    name = models.CharField(max_length=60)
    acronym = models.CharField(max_length=10)
