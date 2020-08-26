import unittest

from django.contrib.auth.models import User
from django.test import TestCase
from django.contrib.auth.models import Group

from organizations.models import Organization, Dorm
from security.models import create_user_to_log_in, User_Associate_with_Organization, User_Associate_with_Dorm, Supervisor, Student
from users.models import CustomUser


class Test_check_requirement(TestCase):

    @classmethod
    def setUpClass(cls):
        TestCase.setUpClass()
        cls.users = {}
        cls.users["test_student"] = CustomUser.objects.create_user("test_student","123")
        cls.users["test_supervisor"] = CustomUser.objects.create_user("test_supervisor","123")
        cls.users["test_student"].save()
        cls.users["test_supervisor"].save()

        cls.organizations = {}
        cls.organizations["PK"] = Organization.objects.create(name="Politechnika Krakowska", acronym="PK")
        cls.organizations["PK"].save()

        cls.dorms = {}
        cls.dorms["DS2 Leon"] = (Dorm.objects.create(name="DS2 Leon"))
        cls.dorms["DS2 Leon"].save()

        User_Associate_with_Organization.associate("test_student", "PK")
        User_Associate_with_Organization.associate("test_supervisor", "PK")
        User_Associate_with_Dorm.associate("test_student", "DS2 Leon")

        group = Group.objects.create(name='students')
        group.save()
        group.user_set.add(cls.users["test_student"])

        group = Group.objects.create(name='supervisors')
        group.save()
        group.user_set.add(cls.users["test_supervisor"])

    def test_check_student_requirements(self):
        loggingInUser = create_user_to_log_in(self.users["test_student"])

        self.assertTrue(loggingInUser.check_requirement(self.users["test_student"], self.organizations["PK"].id, self.dorms["DS2 Leon"].name))

        self.assertFalse(loggingInUser.check_requirement(self.users["test_student"], self.organizations["PK"].id, "wrong dorm name"))
        self.assertFalse(loggingInUser.check_requirement(self.users["test_student"], 0, self.dorms["DS2 Leon"].name))
        self.assertFalse(loggingInUser.check_requirement(CustomUser.objects.create(email="user with out association",password='123'), self.organizations["PK"].id, self.dorms["DS2 Leon"].name))

    def test_check_supervisor_requirements(self):
        loggingInUser = create_user_to_log_in(self.users["test_supervisor"])

        self.assertTrue(loggingInUser.check_requirement(self.users["test_supervisor"], self.organizations["PK"].id, self.dorms["DS2 Leon"].name))
        self.assertTrue(loggingInUser.check_requirement(self.users["test_supervisor"], self.organizations["PK"].id, "wrong dorm name"))

        self.assertFalse(loggingInUser.check_requirement(self.users["test_supervisor"], 0, self.dorms["DS2 Leon"].name))
        self.assertFalse(loggingInUser.check_requirement(CustomUser.objects.create(email="user with out association",password="123"), self.organizations["PK"].id, self.dorms["DS2 Leon"].name))


class Test_create_user_to_log_in(TestCase):

    @classmethod
    def setUpClass(cls):
        TestCase.setUpClass()
        cls.users = {}
        cls.users["test_student"] = CustomUser.objects.create_user("test_student", "123")
        cls.users["test_supervisor"] = CustomUser.objects.create_user("test_supervisor", "123")
        cls.users["test_student"].save()
        cls.users["test_supervisor"].save()

        cls.organizations = {}
        cls.organizations["PK"] = Organization.objects.create(name="Politechnika Krakowska", acronym="PK")
        cls.organizations["PK"].save()

        cls.dorms = {}
        cls.dorms["DS2 Leon"] = (Dorm.objects.create(name="DS2 Leon"))
        cls.dorms["DS2 Leon"].save()

        User_Associate_with_Organization.associate("test_student", "PK")
        User_Associate_with_Organization.associate("test_supervisor", "PK")
        User_Associate_with_Dorm.associate("test_student", "DS2 Leon")

        group = Group.objects.create(name='students')
        group.save()
        group.user_set.add(cls.users["test_student"])

        group = Group.objects.create(name='supervisors')
        group.save()
        group.user_set.add(cls.users["test_supervisor"])

    def test_check_created_type_for_supervisor(self):
        loggingInUser = create_user_to_log_in(self.users["test_supervisor"])
        self.assertEqual(type(loggingInUser), Supervisor)

    def test_check_created_for_student(self):
        loggingInUser = create_user_to_log_in(self.users["test_student"])
        self.assertEqual(type(loggingInUser), Student)

    def test_created_user_without_group(self):
        userWithoutGroup = CustomUser.objects.create(email="user_without_group",password="123")

        with self.assertRaises(ValueError):
            create_user_to_log_in(userWithoutGroup)

    def test_created_user_with_wrong_group(self):
        user = CustomUser.objects.create(email="user_with_wrong_group",password="123")
        self._prepare_wrong_group(user)

        with self.assertRaises(ValueError):
            create_user_to_log_in(user)

    def _prepare_wrong_group(self, user):
        group = Group.objects.create(name='wrong group name')
        group.save()
        group.user_set.add(user)
