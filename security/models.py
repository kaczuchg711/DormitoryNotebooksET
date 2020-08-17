from abc import ABC

from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.
from organizations.models import Organization, Dorm


def create_user_to_log_in(user: User):
    # Todo test this
    groups = user.groups.all()
    if Group.objects.filter(name="supervisors")[0] in groups:
        return Supervisor()
    elif Group.objects.filter(name="students")[0] in groups:
        return Student()


class ICheckerRequirement(ABC):
    def check_requirement(self, organizationID, dormName):
        pass


class Student(models.Model):
    __metaclass__ = ICheckerRequirement

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    room = models.IntegerField()

    def check_requirement(self, user, organizationID, dormName):
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

        if User_Associate_with_Organization.association_exist(organization.get_id(), user.id):
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

    @staticmethod
    def associate(userLogin,dormName):
        association = User_Associate_with_Dorm()

        user = User.objects.filter(username=userLogin)[0]
        association.id_user = user

        dorm = Dorm.objects.filter(name=dormName)[0]
        association.id_dorm = dorm

        if User_Associate_with_Dorm.association_exist(dorm.get_id(), user.id):
            pass
        else:
            association.save()


