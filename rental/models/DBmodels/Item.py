from django.db import models
from organizations.models import Dorm


class Item(models.Model):
    name = models.CharField(max_length=255)
    number = models.IntegerField(default=0)
    dorm = models.ForeignKey(Dorm, on_delete=models.CASCADE)
    isAvailable = models.BooleanField(default=True)

