from django.db import models

# Create your models here.
from organizations.models import Dorm
from users.models import CustomUser


class Breakdowns(models.Model):
    requestDate = models.DateField(default=None)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.CharField(max_length=600)
    isSolved = models.BooleanField(default=False)
    dorm = models.ForeignKey(Dorm, on_delete=models.CASCADE)

