from unittest import TestCase

from django.test import TestCase
from django.contrib.auth.models import User

from organizations.models import Organization
from security.models import create_user_to_log_in, User_Associate_with_Organization

# Create your tests here.

class Test(TestCase):
    def test_User_Associate_with_Organization(self):
        user, organization = self._prepare_data()

        User_Associate_with_Organization.associate('john', 'pk')
        resultOrganizationID = User_Associate_with_Organization.objects.values('id_organization').filter(id_user=user.id)[0]['id_organization']

        self.assertEqual(organization.id, resultOrganizationID)


    def _prepare_data(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.save()
        organization = Organization.objects.create(acronym='pk')
        organization.save()
        return user, organization
