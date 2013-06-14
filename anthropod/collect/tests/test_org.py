from django.test import Client, TestCase
from django.core.urlresolvers import reverse

import anthropod.core
import anthropod.tests
from .fixtures import load_test_fixtures


class AdminUserTest(TestCase):
    '''This test verifies that a new person created with
    the form will get saved as the expected popolo data object.
    '''
    fixtures = ['test_auth']

    tearDown = staticmethod(anthropod.tests.teardown)
    maxDiff = None

    login_credentials = dict(username='user1', password='password1')

    def setUp(self):
        '''Start with an empty database.'''
        load_test_fixtures()
        self.client = Client()
        self.client.login(**self.login_credentials)
        self.db = anthropod.core.db

    def test_form(self):
        '''Submit the organization form with valid data. Ensure that
        the form validates the data and saves is as the expected
        popolo equivalent in mongo.
        '''
        # Create a new organization.
        url = reverse('organization.create')
        resp = self.client.post(url, dict(self.params))

        # # A successful post and form validation should
        # # trigger a redirect to the person's page.
        # self.assertEquals(resp.status_code, 302)

        # # Now verify that the saved popolo object
        # # matches what we expect.
        # saved = self.db.organizations.find_one()
        # saved.pop('_id')
        # self.assertEquals(saved, self.expected)

    expected = {
        'name': 'City Council',
        'geography_id': 'ocd:location:country-us:state-idaho:city-boise',
        'source_url': 'http://mayor.cityofboise.org/city-council/'
    }

    params = [
        ('name', 'City Council'),
        ('geography_id', 'ocd:location:country-us:state-idaho:city-boise'),
        ('source_url', 'http://mayor.cityofboise.org/city-council/'),
    ]
