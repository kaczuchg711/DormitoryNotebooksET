from abc import ABC


class ICheckerRequirement(ABC):
    def check_requirement(self, organizationID, dormName):
        pass