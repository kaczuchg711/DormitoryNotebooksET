from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from organizations.models import Organization, Dorm


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    room = models.IntegerField()


class User_Associate_with_Organization(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_organization = models.ForeignKey(Organization, on_delete=models.SET(0))

class User_Associate_with_Dorm(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_dorm = models.ForeignKey(Dorm, on_delete=models.SET(0))

