from organizations.models import Dorm
from security.models.DBmodels.User_Associate_with_Dorm import User_Associate_with_Dorm
from security.models.DBmodels.User_Associate_with_Organization import User_Associate_with_Organization
from security.models.NonDBmodels.ICheckerRequirement import ICheckerRequirement


class Student:
    __metaclass__ = ICheckerRequirement

    def check_requirement(self, user, organizationID, dormName):
        if Dorm.dorm_exist(dormName):
            dormID = Dorm.objects.filter(name=dormName)[0].id
            if User_Associate_with_Organization.association_exist(organizationID, user.id) and \
                    User_Associate_with_Dorm.association_exist(dormID, user.id):
                return True
        return False
