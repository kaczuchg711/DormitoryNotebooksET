from django.db import models


# Create your models here.

class Organization(models.Model):
    name = models.CharField(max_length=60)
    acronym = models.CharField(max_length=10)

    @staticmethod
    def get_every_organizations_paths_to_logos():
        acronyms = Organization.get_every_organizations_acronyms()
        imgPath = ["img/" + path + "_logo.png" for path in acronyms]
        return imgPath

    @staticmethod
    def get_every_organizations_acronyms():
        querySet = Organization.objects.values('acronym')
        acronyms = [j['acronym'] for j in [i for i in querySet]]
        return acronyms

    def get_dorms_names(self):
        # Todo make this clean
        organizationsDormitoriesIdsQS = Dorm_associative_Oraganaizor.objects.values('id_dorm').filter(
            id_organization=self.id)
        organizationsDormitoriesIds = [j['id_dorm'] for j in [i for i in organizationsDormitoriesIdsQS]]

        DormsObjects = Dorm.objects.all()
        list = []
        for i in organizationsDormitoriesIds:
            list.append(DormsObjects.filter(id = i).values('name'))

        organizationsDormitoriesNames = [i[0]['name'] for i in list]

        return organizationsDormitoriesNames

    def get_id(self):
        return self.id


class Dorm(models.Model):
    name = models.CharField(max_length=60)


class Dorm_associative_Oraganaizor(models.Model):
    id_dorm = models.ForeignKey(Dorm, on_delete=models.SET(0))
    id_organization = models.ForeignKey(Organization, on_delete=models.SET(0))
