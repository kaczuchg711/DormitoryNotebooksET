from django.db import models

# Create your models here.
from django.shortcuts import redirect

from global_fun import change_QuerySet_from_db_to_list


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
        acronyms = change_QuerySet_from_db_to_list(querySet, 'acronym')
        return acronyms

    @staticmethod
    def organization_in_db(acronym):
        acronyms = Organization.get_every_organizations_acronyms()
        return True if acronym in acronyms else False

    @staticmethod
    def set_organization(request):
        organizationAcronym = request.POST.get('organization')
        if Organization.organization_in_db(organizationAcronym):
            organization = Organization.objects.filter(acronym=organizationAcronym)[0]
            request.session['organization_id'] = organization.get_id()
            return redirect('/')
        else:
            return redirect('organization')



    def get_dorms_names(self):
        organizationsDormitoriesIdsQS = Associate_with_Dorms.objects.values('id_dorm').filter(id_organization=self.id)
        organizationsDormitoriesIds = change_QuerySet_from_db_to_list(organizationsDormitoriesIdsQS, 'id_dorm')

        DormsObjects = Dorm.objects.all()
        querySets = []
        for i in organizationsDormitoriesIds:
            querySets.append(DormsObjects.filter(id=i).values('name'))

        organizationsDormitoriesNames = [i[0]['name'] for i in querySets]

        return organizationsDormitoriesNames

    def get_id(self):
        return self.id



class Dorm(models.Model):
    name = models.CharField(max_length=60)

    @staticmethod
    def dorm_exist(dormName):
        dorms = list(Dorm.objects.filter(name=dormName))
        if len(dorms) != 0:
            return True
        return False

    @staticmethod
    def get_dorm_id(dormName):
        dorms = list(Dorm.objects.filter(name=dormName))
        return dorms[0].get_id()


    def get_id(self):
        return self.id


class Associate_with_Dorms(models.Model):
    id_dorm = models.ForeignKey(Dorm, on_delete=models.SET(0))
    id_organization = models.ForeignKey(Organization, on_delete=models.SET(0))
