from django.db import models

# Create your models here.
from django.shortcuts import redirect, render

from global_fun import get_column_values


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
        acronyms = get_column_values(querySet, 'acronym')
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
            request.session['organization_id'] = organization.id
            return redirect('/')
        else:
            return redirect('organization')

    def get_dorms_names(self):
        organizationsDormitoriesIdsQS = Associate_with_Dorms.objects.values('id_dorm').filter(id_organization=self.id)
        organizationsDormitoriesIds = get_column_values(organizationsDormitoriesIdsQS, 'id_dorm')

        DormsObjects = Dorm.objects.all()
        querySets = []
        for i in organizationsDormitoriesIds:
            querySets.append(DormsObjects.filter(id=i).values('name'))

        organizationsDormitoriesNames = [i[0]['name'] for i in querySets]

        return organizationsDormitoriesNames


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
        return dorms[0].id


class Associate_with_Dorms(models.Model):
    id_dorm = models.ForeignKey(Dorm, on_delete=models.SET(0))
    id_organization = models.ForeignKey(Organization, on_delete=models.SET(0))

    @staticmethod
    def associate(dormName, organizationAcronym):
        association = Associate_with_Dorms()
        x = 1
        dorm = Dorm.objects.filter(name=dormName)[0]
        organization = Organization.objects.filter(acronym=organizationAcronym)[0]

        association.id_dorm = dorm
        association.id_organization = organization

        if Associate_with_Dorms.association_exist(dorm.id, organization.id):
            Warning("association_exist")
        else:
            association.save()

    @staticmethod
    def association_exist(dorm_id, organization_id):
        if len(Associate_with_Dorms.objects.filter(id_dorm_id=dorm_id, id_organization_id=organization_id)) != 0:
            return True
        return False