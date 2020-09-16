from security.models.fun import create_user_to_log_in
from security.tests.TestCaseWithDefaultDB import TestCaseWithDefaultDB
from users.models import CustomUser


class TestCheckRequirement(TestCaseWithDefaultDB):
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
