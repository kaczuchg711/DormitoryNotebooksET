from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from organizations.models import Dorm


class RentItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dorm = models.ForeignKey(Dorm, on_delete=models.CASCADE)
    itemName = models.CharField(max_length=255)
    rentalDate = models.DateField(default=None)
    rentHour = models.TimeField(default=None)
    returnHour = models.TimeField(default=None)

