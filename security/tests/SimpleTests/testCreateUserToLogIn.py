from django.contrib.auth.models import Group

from security.models.fun import create_user_to_log_in
from security.models.NonDBmodels.Supervisor import Supervisor
from security.models.NonDBmodels.Student import Student
from security.tests.TestCaseWithDefaultDB import TestCaseWithDefaultDB
from users.models import CustomUser

class TestCreateUserToLogIn(TestCaseWithDefaultDB):
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
