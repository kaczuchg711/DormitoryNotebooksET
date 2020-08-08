from django.db import models


# Create your models here.

class Organization(models.Model):
    name = models.CharField(max_length=60)
    acronym = models.CharField(max_length=10)

class Dorm(models.Model):
    name = models.CharField(max_length=60)

class Dorm_associative_Oraganaizor(models.Model):
    id_dorm = models.ForeignKey(Dorm, on_delete=models.SET(0))
    id_organization = models.ForeignKey(Organization, on_delete=models.SET(0))