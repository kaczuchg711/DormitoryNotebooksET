# selinum
from time import sleep

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
            "test_student": CustomUser.objects.create_user("test_student", "correctPassword"),
            "test_supervisor": CustomUser.objects.create_user("test_supervisor", "correctPassword")
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

        self.organizations = {"UJ": Organization.objects.create(name="Uniwersytet Jagieloński", acronym="UJ")}
        self.organizations["UJ"].save()

        self.dorms = {
            "Żaczek": Dorm.objects.create(name="Żaczek"),
            "Piast": Dorm.objects.create(name="Piast")
        }
        self.dorms["Żaczek"].save()
        self.dorms["Piast"].save()

        Associate_with_Dorms.associate("Żaczek", "UJ")
        Associate_with_Dorms.associate("Piast", "UJ")

        User_Associate_with_Organization.associate("test_student", "PK")
        User_Associate_with_Organization.associate("test_supervisor", "PK")
        User_Associate_with_Dorm.associate("test_student", "DS2 Leon")

        group = Group.objects.create(name='students')
        group.save()
        group.user_set.add(self.users["test_student"])

        group = Group.objects.create(name='supervisors')
        group.save()
        group.user_set.add(self.users["test_supervisor"])

    def test_student_log_in_with_correct_data(self):
        # build
        self.driver.get(self.live_server_url)
        # operate
        self._pass_logIn_sites("PK", "DS2 Leon", "test_student", "correctPassword")
        # check
        self.assertEqual("choice", self.driver.title)

    def test_student_log_in_with_wrong_password(self):
        # build
        self.driver.get(self.live_server_url)
        # operate
        self._pass_logIn_sites("PK", "DS2 Leon", "test_student", "wrongPassword")
        # check
        self.assertEqual("home", self.driver.title)

    def test_student_log_in_with_wrong_email(self):
        # build
        self.driver.get(self.live_server_url)
        # operate
        self._pass_logIn_sites("PK", "DS2 Leon", "wrong_email", "correctPassword")
        # check
        self.assertEqual("home", self.driver.title)

    def test_student_log_in_with_wrong_dorm_name(self):
        # build
        self.driver.get(self.live_server_url)
        # operate
        self._pass_logIn_sites("PK", "DS1 Rumcajs", "test_student", "correctPassword")
        # check
        self.assertEqual("home", self.driver.title)

    def test_student_log_in_with_wrong_organization_acronym(self):
        # build
        self.driver.get(self.live_server_url)
        # operate
        self._pass_logIn_sites("UJ", "Żaczek", "test_student", "correctPassword")
        # check
        self.assertEqual("home", self.driver.title)

    def test_supervisor_log_in_with_correct_data(self):
        # build
        self.driver.get(self.live_server_url)
        # operate
        self._pass_logIn_sites("PK", "DS2 Leon", "test_supervisor", "correctPassword")
        # check
        self.assertEqual("choice", self.driver.title)

    def test_supervisor_log_in_with_wrong_email(self):
        # build
        self.driver.get(self.live_server_url)
        # operate
        self._pass_logIn_sites("PK", "DS2 Leon", "wrong_email", "correctPassword")
        # check
        self.assertEqual("home", self.driver.title)

    def test_supervisor_log_in_with_different_dorm_name(self):
        # build
        self.driver.get(self.live_server_url)
        # operate
        self._pass_logIn_sites("PK", "DS1 Rumcajs", "test_supervisor", "correctPassword")
        # check
        self.assertEqual("choice", self.driver.title)

    def test_supervisor_log_in_with_wrong_organization_acronym(self):
        # build
        self.driver.get(self.live_server_url)
        # operate
        self._pass_logIn_sites("UJ", "Żaczek", "test_supervisor", "correctPassword")
        # check
        self.assertEqual("home", self.driver.title)



    def _pass_logIn_sites(self, organizationAcronym, dormName, email, password):
        button = self.driver.find_element_by_id(organizationAcronym)
        button.click()
        self.driver.find_element_by_xpath("//select[@name='dorms']/option[text()='" + dormName + "']").click()
        emailInput = self.driver.find_element_by_name("email")
        emailInput.send_keys(email)
        passwordInput = self.driver.find_element_by_name("password")
        passwordInput.send_keys(password)
        self.driver.find_element_by_name("submit").click()

    def tearDown(self):
        self.driver.close()
