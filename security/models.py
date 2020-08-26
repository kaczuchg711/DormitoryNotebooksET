from abc import ABC

from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.
from django_mysql.models import QuerySet

from organizations.models import Organization, Dorm
from users.models import CustomUser


def create_user_to_log_in(user: User):
    user_groups = user.groups.all()
    groups = Group.objects.all()
    user_groups:QuerySet

    if len(user_groups) == 0:
        raise ValueError
    elif all(x in groups.filter(name="supervisors") for x in user_groups):
        return Supervisor()
    elif all(x in groups.filter(name="students") for x in user_groups):
        return Student()
    else:
        raise ValueError


class ICheckerRequirement(ABC):
    def check_requirement(self, organizationID, dormName):
        pass


class Student:
    __metaclass__ = ICheckerRequirement

    def check_requirement(self, user, organizationID, dormName):
        if Dorm.dorm_exist(dormName):
            dormID = Dorm.objects.filter(name=dormName)[0].get_id()
            if User_Associate_with_Organization.association_exist(organizationID, user.id) and \
                    User_Associate_with_Dorm.association_exist(dormID, user.id):
                return True
        return False


class Supervisor:
    __metaclass__ = ICheckerRequirement

    def check_requirement(self, user, organizationID, dormName):
        if User_Associate_with_Organization.association_exist(organizationID, user.id):
            return True
        return False


class User_Associate_with_Organization(models.Model):
    id_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    id_organization = models.ForeignKey(Organization, on_delete=models.SET(0))

    @staticmethod
    def association_exist(organizationId, user_id):
        if len(User_Associate_with_Organization.objects.filter(id_organization_id=organizationId, id_user_id=user_id)) != 0:
            return True
        return False

    @staticmethod
    def associate(useremail, organizationAcronym):
        association = User_Associate_with_Organization()

        user = CustomUser.objects.filter(email=useremail)[0]
        organization = Organization.objects.filter(acronym=organizationAcronym)[0]

        association.id_user = user
        association.id_organization = organization

        if User_Associate_with_Organization.association_exist(organization.get_id(), user.id):
            pass
        else:
            association.save()


class User_Associate_with_Dorm(models.Model):
    id_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    id_dorm = models.ForeignKey(Dorm, on_delete=models.SET(0))

    @staticmethod
    def association_exist(dorm_id, user_id):
        if len(User_Associate_with_Dorm.objects.filter(id_dorm_id=dorm_id, id_user=user_id)) != 0:
            return True
        return False

    @staticmethod
    def associate(userEmail, dormName):
        association = User_Associate_with_Dorm()

        user = CustomUser.objects.filter(email=userEmail)[0]
        association.id_user = user

        dorm = Dorm.objects.filter(name=dormName)[0]
        association.id_dorm = dorm

        if User_Associate_with_Dorm.association_exist(dorm.get_id(), user.id):
            pass
        else:
            association.save()
