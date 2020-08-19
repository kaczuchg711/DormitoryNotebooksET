from django.contrib.auth.models import User
from django.test import TestCase
from django.contrib.auth.models import Group

from organizations.models import Organization, Dorm
from security.models import create_user_to_log_in, User_Associate_with_Organization, User_Associate_with_Dorm


class Test_check_requirement(TestCase):

    def setUp(self):
        self.users = {}
        self.users["test_student"] = User.objects.create_user("test_student")
        self.users["test_supervisor"] = User.objects.create_user("test_supervisor")
        self.users["test_student"].save()
        self.users["test_supervisor"].save()

        self.organizations = {}
        self.organizations["PK"] = Organization.objects.create(name="Politechnika Krakowska", acronym="PK")
        self.organizations["PK"].save()

        self.dorms = {}
        self.dorms["DS2 Leon"] = (Dorm.objects.create(name="DS2 Leon"))
        self.dorms["DS2 Leon"].save()

        User_Associate_with_Organization.associate("test_student", "PK")
        User_Associate_with_Organization.associate("test_supervisor", "PK")
        User_Associate_with_Dorm.associate("test_student", "DS2 Leon")

        group = Group.objects.create(name='students')
        group.save()
        group.user_set.add(self.users["test_student"])


        group = Group.objects.create(name='supervisors')
        group.save()
        group.user_set.add(self.users["test_supervisor"])



    def test_check_student_requirements(self):
        loggingInUser = create_user_to_log_in(self.users["test_student"])

        self.assertTrue(loggingInUser.check_requirement(self.users["test_student"], self.organizations["PK"].id, self.dorms["DS2 Leon"].name))

        self.assertFalse(loggingInUser.check_requirement(self.users["test_student"], self.organizations["PK"].id, "wrong dorm name"))
        self.assertFalse(loggingInUser.check_requirement(self.users["test_student"], 0, self.dorms["DS2 Leon"].name))
        self.assertFalse(loggingInUser.check_requirement(User.objects.create(username="user with out association"), self.organizations["PK"].id, self.dorms["DS2 Leon"].name))

    def test_check_supervisor_requirements(self):
        loggingInUser = create_user_to_log_in(self.users["test_supervisor"])

        self.assertTrue(loggingInUser.check_requirement(self.users["test_supervisor"], self.organizations["PK"].id, self.dorms["DS2 Leon"].name))
        self.assertTrue(loggingInUser.check_requirement(self.users["test_supervisor"], self.organizations["PK"].id, "wrong dorm name"))

        self.assertFalse(loggingInUser.check_requirement(self.users["test_supervisor"], 0, self.dorms["DS2 Leon"].name))
        self.assertFalse(loggingInUser.check_requirement(User.objects.create(username="user with out association"), self.organizations["PK"].id, self.dorms["DS2 Leon"].name))
