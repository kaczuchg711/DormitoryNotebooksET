# selinum
from time import sleep

from django.contrib.auth.models import Group
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.test import TestCase, SimpleTestCase, LiveServerTestCase

from organizations.models import Organization, Dorm, Associate_with_Dorms
from security.models import User_Associate_with_Organization, User_Associate_with_Dorm
from security.tests.model_tests import SetterTestDataBase
from users.models import CustomUser


class TestFoo(StaticLiveServerTestCase):

    def setUp(self):
        StaticLiveServerTestCase.setUp(self)

        self.driver = webdriver.Firefox(executable_path=r'security/tests/geckodriver')

        self.users = {}
        self.users["test_student"] = CustomUser.objects.create_user("test_student", "123")
        self.users["test_supervisor"] = CustomUser.objects.create_user("test_supervisor", "123")
        self.users["test_student"].save()
        self.users["test_supervisor"].save()

        self.organizations = {}
        self.organizations["PK"] = Organization.objects.create(name="Politechnika Krakowska", acronym="PK")
        self.organizations["PK"].save()

        self.dorms = {}
        self.dorms["DS1 Rumcajs"] = Dorm.objects.create(name="DS1 Rumcajs")
        self.dorms["DS2 Leon"] = Dorm.objects.create(name="DS2 Leon")
        self.dorms["DS1 Rumcajs"].save()
        self.dorms["DS2 Leon"].save()

        Associate_with_Dorms.associate("DS1 Rumcajs", "PK")
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

    def test_foo(self):
        # todo clean this
        self.driver.get(self.live_server_url)
        button = self.driver.find_element_by_id("PK")
        button.click()
        self.driver.find_element_by_xpath("//select[@name='dorms']/option[text()='DS2 Leon']").click()
        emailInput = self.driver.find_element_by_name("email")
        emailInput.send_keys("test_student")
        passwordInput = self.driver.find_element_by_name("password")
        passwordInput.send_keys("123")
        self.driver.find_element_by_name("submit").click()
        sleep(1)
        self.assertEqual(self.driver.title,"choice")
    def tearDown(self):
        self.driver.close()
