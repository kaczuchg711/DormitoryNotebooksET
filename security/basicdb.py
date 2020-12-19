from time import sleep

from django.shortcuts import redirect

from organizations.models import Organization, Dorm, Associate_with_Dorms


class BasicDB:

    def __init__(self):
        self.dorms = {}

    def create_organizations(self):
        if not Organization.organization_in_db("PK"):
            Organization(name="Politechnika Krakowska", acronym="PK").save()
        if not Organization.organization_in_db("UJ"):
            Organization(name="Uniwersytet Jagieloński ", acronym="UJ").save()
        if not Organization.organization_in_db("AGH"):
            Organization(name="Akademia Górniczo Hutnicza", acronym="AGH").save()

    def create_dorms(self):

        self.dorms = {
            "PK" : ("DS B1 Bydgoska", "DS1 Rumcajs", "DS2 Leon", "DS3 Bartek", "DS4 Balon"),
            "UJ" : ("Akademik UJ1", "Akademik UJ2"),
            "AGH": ("Olimp", "Akropol", "Hajduczek"),
        }

        organizations_acronyms = self.dorms.keys()

        for acronym in organizations_acronyms:
            self.dorms[acronym] = []
            for name in self.dorms[acronym]:
                created_dorms = [x.name for x in Dorm.objects.all()]
                if name in created_dorms:
                    continue
                dorm = Dorm(name=name)
                dorm.save()

    def associate_dorms_with_organization(self):
        for organization_acronym in self.dorms.keys():
            for dorm in self.dorms[organization_acronym]:
                Associate_with_Dorms.associate(dorm.name, organization_acronym)


def create_basic_db(request):
    db = BasicDB()
    db.create_organizations()
    db.create_dorms()
    db.associate_dorms_with_organization()
    # todo users
    # todo items
    return redirect("organization")
