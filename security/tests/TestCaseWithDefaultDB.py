from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from organizations.models import Organization, Dorm, Associate_with_Dorms
from security.models.DBmodels.User_Associate_with_Dorm import User_Associate_with_Dorm
from security.models.DBmodels.User_Associate_with_Organization import User_Associate_with_Organization
from users.models import CustomUser


class TestCaseWithDefaultDB(TestCase):
    def setUp(self):
        self.login_url = reverse('index')

        self.users = {}
        self.users["test_student"] = CustomUser.objects.create_user("test_student", "123")
        self.users["test_supervisor"] = CustomUser.objects.create_user("test_supervisor", "123")
        self.users["test_student"].save()
        self.users["test_supervisor"].save()

        self.organizations = {}
        self.organizations["PK"] = Organization.objects.create(name="Politechnika Krakowska", acronym="PK")
        self.organizations["PK"].save()

        self.dorms = {}
        self.dorms["DS2 Leon"] = (Dorm.objects.create(name="DS2 Leon"))
        self.dorms["DS2 Leon"].save()

        Associate_with_Dorms.associate("DS2 Leon", "PK")

        User_Associate_with_Organization.associate("test_student", "PK")
        User_Associate_with_Organization.associate("test_supervisor", "PK")
        User_Associate_with_Dorm.associate("test_student", "DS2 Leon")

        group = Group.objects.create(name='students')
        group.save()
        group.user_set.add(self.users["test_student"])

        group = Group.objects.create(name='supervisors')
        group.save()
        group.user_set.add(self.users["test_supervisor"])
