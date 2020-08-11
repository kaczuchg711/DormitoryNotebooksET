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

    @staticmethod
    def association_exist(organizationId, user_id):
        if len(User_Associate_with_Organization.objects.filter(id_organization_id=organizationId, id_user_id=user_id)) != 0:
            return True
        return False

    @staticmethod
    def associate(userLogin, organizationAcronym):
        association = User_Associate_with_Organization()

        user = User.objects.filter(username=userLogin)[0]
        organization = Organization.objects.filter(acronym=organizationAcronym)[0]

        association.id_user = user
        association.id_organization = organization

        if User_Associate_with_Organization.association_exist(organization.get_id(),user.id):
            pass
        else:
            association.save()






class User_Associate_with_Dorm(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_dorm = models.ForeignKey(Dorm, on_delete=models.SET(0))

    @staticmethod
    def association_exist(dorm_id, user_id):
        if len(User_Associate_with_Dorm.objects.filter(id_dorm_id=dorm_id, id_user=user_id)) != 0:
            return True
        return False
