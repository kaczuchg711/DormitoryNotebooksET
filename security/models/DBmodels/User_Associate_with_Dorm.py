from django.db import models

from organizations.models import Dorm
from users.models import CustomUser


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

        if User_Associate_with_Dorm.association_exist(dorm.id, user.id):
            pass
        else:
            association.save()