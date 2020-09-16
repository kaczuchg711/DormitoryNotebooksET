from security.tests.TestCaseWithDefaultDB import TestCaseWithDefaultDB


class TestPrepareLogIn(TestCaseWithDefaultDB):
    def test_redirect_to_organization(self):
        response = self.client.post(self.login_url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'security/organization.html')

    def test_can_gain_access_to_home_page(self):
        self._choose_organization()

        response = self.client.post('', {})

        self.assertTemplateUsed(response, 'security/home.html')

    def _choose_organization(self):
        session = self.client.session
        session['organization_id'] = self.organizations['PK'].id
        session.save()
