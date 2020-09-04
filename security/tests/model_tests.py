import unittest
from time import sleep

from django.contrib.auth.models import User
from django.test import TestCase, SimpleTestCase, LiveServerTestCase
from django.contrib.auth.models import Group
from django.urls import reverse



from organizations.models import Organization, Dorm, Associate_with_Dorms
from security.models import create_user_to_log_in, User_Associate_with_Organization, User_Associate_with_Dorm, Supervisor, Student
from users.models import CustomUser


class SetterTestDataBase:
    def setUp(self):
        TestCase.setUpClass()
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

        Associate_with_Dorms.associate("DS2 Leon","PK")

        User_Associate_with_Organization.associate("test_student", "PK")
        User_Associate_with_Organization.associate("test_supervisor", "PK")
        User_Associate_with_Dorm.associate("test_student", "DS2 Leon")

        group = Group.objects.create(name='students')
        group.save()
        group.user_set.add(self.users["test_student"])

        group = Group.objects.create(name='supervisors')
        group.save()
        group.user_set.add(self.users["test_supervisor"])


class Test_check_requirement(SetterTestDataBase,TestCase):

    def test_check_student_requirements(self):
        loggingInUser = create_user_to_log_in(self.users["test_student"])

        self.assertTrue(loggingInUser.check_requirement(self.users["test_student"], self.organizations["PK"].id, self.dorms["DS2 Leon"].name))

        self.assertFalse(loggingInUser.check_requirement(self.users["test_student"], self.organizations["PK"].id, "wrong dorm name"))
        self.assertFalse(loggingInUser.check_requirement(self.users["test_student"], 0, self.dorms["DS2 Leon"].name))
        self.assertFalse(loggingInUser.check_requirement(CustomUser.objects.create(email="user with out association", password='123'), self.organizations["PK"].id, self.dorms["DS2 Leon"].name))

    def test_check_supervisor_requirements(self):
        loggingInUser = create_user_to_log_in(self.users["test_supervisor"])

        self.assertTrue(loggingInUser.check_requirement(self.users["test_supervisor"], self.organizations["PK"].id, self.dorms["DS2 Leon"].name))
        self.assertTrue(loggingInUser.check_requirement(self.users["test_supervisor"], self.organizations["PK"].id, "wrong dorm name"))

        self.assertFalse(loggingInUser.check_requirement(self.users["test_supervisor"], 0, self.dorms["DS2 Leon"].name))
        self.assertFalse(loggingInUser.check_requirement(CustomUser.objects.create(email="user with out association", password="123"), self.organizations["PK"].id, self.dorms["DS2 Leon"].name))


class Test_create_user_to_log_in(SetterTestDataBase,TestCase):

    def test_check_created_type_for_supervisor(self):
        loggingInUser = create_user_to_log_in(self.users["test_supervisor"])
        self.assertEqual(type(loggingInUser), Supervisor)

    def test_check_created_for_student(self):
        loggingInUser = create_user_to_log_in(self.users["test_student"])
        self.assertEqual(type(loggingInUser), Student)

    def test_created_user_without_group(self):
        userWithoutGroup = CustomUser.objects.create(email="user_without_group", password="123")

        with self.assertRaises(ValueError):
            create_user_to_log_in(userWithoutGroup)

    def test_created_user_with_wrong_group(self):
        user = CustomUser.objects.create(email="user_with_wrong_group", password="123")
        self._prepare_wrong_group(user)

        with self.assertRaises(ValueError):
            create_user_to_log_in(user)

    def _prepare_wrong_group(self, user):
        group = Group.objects.create(name='wrong group name')
        group.save()
        group.user_set.add(user)


class TestLogIn(SetterTestDataBase,TestCase):
    def test_redirect_to_organization(self):
        response = self.client.post(self.login_url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'security/organization.html')

    def test_can_gain_access_to_home_page(self):
        self._choose_organization()

        response = self.client.post('', {})

        self.assertTemplateUsed(response, 'security/home.html')

    def test_log_in(self):
        # Todo finish this
        self._choose_organization()

        email = self.client.POST['email']
        password = self.client.POST['password']

        response = self.client.post('login', {}, follow=True)

        self.assertTemplateUsed(response, 'panel/choice.html')
        pass

    def _choose_organization(self):
        session = self.client.session
        session['organization_id'] = self.organizations['PK'].id
        session.save()


