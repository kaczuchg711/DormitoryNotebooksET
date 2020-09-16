from security.models.DBmodels.User_Associate_with_Organization import User_Associate_with_Organization
from security.models.NonDBmodels.ICheckerRequirement import ICheckerRequirement


class Supervisor:
    __metaclass__ = ICheckerRequirement

    def check_requirement(self, user, organizationID, dormName):
        if User_Associate_with_Organization.association_exist(organizationID, user.id):
            return True
        return False
