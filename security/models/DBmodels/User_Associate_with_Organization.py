from django.db import models

from organizations.models import Organization
from users.models import CustomUser


class User_Associate_with_Organization(models.Model):
    id_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    id_organization = models.ForeignKey(Organization, on_delete=models.SET(0))

    @staticmethod
    def association_exist(organizationId, user_id):
        if len(User_Associate_with_Organization.objects.filter(id_organization_id=organizationId, id_user_id=user_id)) != 0:
            return True
        return False

    @staticmethod
    def associate(userEmail, organizationAcronym):
        association = User_Associate_with_Organization()

        user = CustomUser.objects.filter(email=userEmail)[0]
        organization = Organization.objects.filter(acronym=organizationAcronym)[0]

        association.id_user = user
        association.id_organization = organization

        if User_Associate_with_Organization.association_exist(organization.id, user.id):
            Warning("association_exist")
        else:
            association.save()


