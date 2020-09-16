# selinum

from django.contrib.auth.models import Group
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

from organizations.models import Organization, Dorm, Associate_with_Dorms
from security.models.DBmodels.User_Associate_with_Dorm import User_Associate_with_Dorm
from security.models.DBmodels.User_Associate_with_Organization import User_Associate_with_Organization
from users.models import CustomUser


class TestLogIn(StaticLiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox(executable_path=r'drivers/geckodriver')

        self.users = {
            "test_student": CustomUser.objects.create_user("test_student", "123"),
            "test_supervisor": CustomUser.objects.create_user("test_supervisor", "123")
        }
        self.users["test_student"].save()
        self.users["test_supervisor"].save()

        self.organizations = {"PK": Organization.objects.create(name="Politechnika Krakowska", acronym="PK")}
        self.organizations["PK"].save()

        self.dorms = {
            "DS1 Rumcajs": Dorm.objects.create(name="DS1 Rumcajs"),
            "DS2 Leon": Dorm.objects.create(name="DS2 Leon")
        }
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

    def test_log_in(self):
        # build
        self.driver.get(self.live_server_url)
        # operate
        self._pass_logIn_sites()
        # check
        self.assertEqual(self.driver.title, "choice")

    def _pass_logIn_sites(self):
        button = self.driver.find_element_by_id("PK")
        button.click()
        self.driver.find_element_by_xpath("//select[@name='dorms']/option[text()='DS2 Leon']").click()
        emailInput = self.driver.find_element_by_name("email")
        emailInput.send_keys("test_student")
        passwordInput = self.driver.find_element_by_name("password")
        passwordInput.send_keys("123")
        self.driver.find_element_by_name("submit").click()

    def tearDown(self):
        self.driver.close()
