from django.contrib.auth.models import User
from django.test import TestCase
from django.contrib.auth.models import Group

from organizations.models import Organization, Dorm
from security.models import create_user_to_log_in, User_Associate_with_Organization, User_Associate_with_Dorm


class Test_check_requirement(TestCase):

    def test_check_student_requirements(self):
        user = User.objects.create_user("test_student")
        user.save()

        organization = Organization.objects.create(name="Politechnika Krakowska", acronym="PK")
        organization.save()

        dorm = Dorm.objects.create(name="DS2 Leon")
        dorm.save()

        User_Associate_with_Organization.associate("test_student", "PK")
        User_Associate_with_Dorm.associate("test_student", "DS2 Leon")

        group = Group.objects.create(name='students')
        group.save()
        group.user_set.add(user)

        loggingInUser = create_user_to_log_in(user)
        # Todo finish this
