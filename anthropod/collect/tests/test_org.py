import re

from django.test import Client, TestCase
from django.core.urlresolvers import reverse, resolve

import anthropod.core
import anthropod.tests

from anthropod.collect.views.organization import jsonview

from .fixtures import load_test_fixtures


class AdminUserTest(TestCase):
    fixtures = ['test_auth.json']
    tearDown = staticmethod(anthropod.tests.teardown)
    maxDiff = None

    login_credentials = dict(username='user1', password='password1')

    def setUp(self):
        '''Load test fixtures and log in before running the tests.'''
        load_test_fixtures()
        self.client = Client()
        self.client.login(**self.login_credentials)
        self.db = anthropod.core.db

    def test_edit(self):
        '''This test verifies that a new person created with
        the form will get saved as the expected popolo data object.
        '''
        # Create a new organization.
        url = reverse('organization.edit')
        resp = self.client.post(url, dict(self.params))

        # Make sure we redirected after the save.
        self.assertEquals(resp.status_code, 302)

        # Verify that the redirect was to the org jsonview.
        location = dict(resp.items())['Location']
        location = re.sub('http://testserver', '', location)
        redirect_view = resolve(location).func
        self.assertEquals(redirect_view, jsonview)

        # Now verify that the saved popolo object
        # matches what we expect.
        ocd_id = re.search(r'ocd-organization.+', location).group()
        ocd_id = ocd_id.rstrip('/')
        saved = self.db.organizations.find_one(ocd_id)
        saved.pop('_id')

        self.assertEquals(saved, self.expected)

    expected = {
        u'_type': u'organization',
        u'contact_details': [
            {u'note': u'Not a real address',
             u'type': u'address',
             u'value': u'123 Example Street'},
            {u'note': u'Fake phone',
             u'type': u'cell',
             u'value': u'(123)456-7890'}],
        u'geography_id': u'ocd-division/country:us/state:id/place:boise_city',
        u'identifiers': [],
        u'name': u'City Council',
        u'posts': [],
        u'sources': [
            {u'note': u'',
             u'url': u'http://mayor.cityofboise.org/city-council/'},
            {u'note': u"Sunlight's url",
             u'url': u'https://sunfoundation.com'}]}

    params = [
        (u'contact_type', ['address', u'cell']),
        (u'contact_note', ['Not a real address', u'Fake phone']),
        (u'contact_value', ['123 Example Street', u'(123)456-7890']),
        (u'source_url', [
            'http://mayor.cityofboise.org/city-council/',
            u'https://sunfoundation.com'
            ]),
        (u'source_note', [
            '',
            u"Sunlight's url"
            ]),
        (u'geography_id', u'ocd-division/country:us/state:id/place:boise_city'),
        (u'name', u'City Council')
        ]



class AuthorizedUserTest(TestCase):
    '''These tests are run as a user isn't an admin but has
    permissions to edit all the objects in the database.
    '''
    fixtures = ['test_auth.json']

    tearDown = staticmethod(anthropod.tests.teardown)
    maxDiff = None

    login_credentials = dict(username='user2', password='password2')

    def setUp(self):
        '''Load test fixtures and log in before running the tests.'''
        load_test_fixtures()
        self.client = Client()
        self.client.login(**self.login_credentials)
        self.db = anthropod.core.db

    def test_edit(self):
        '''This test verifies that a new person created with
        the form will get saved as the expected popolo data object.
        '''
        # Create a new organization.
        url = reverse('organization.edit')
        resp = self.client.post(url, dict(self.params))

        # Make sure we redirected after the save.
        self.assertEquals(resp.status_code, 302)

        # Verify that the redirect was to the org jsonview.
        location = dict(resp.items())['Location']
        location = re.sub('http://testserver', '', location)
        redirect_view = resolve(location).func
        self.assertEquals(redirect_view, jsonview)

        # Now verify that the saved popolo object
        # matches what we expect.
        ocd_id = re.search(r'ocd-organization.+', location).group()
        ocd_id = ocd_id.rstrip('/')
        saved = self.db.organizations.find_one(ocd_id)
        saved.pop('_id')

        self.assertEquals(saved, self.expected)

    expected = {
        u'_type': u'organization',
        u'contact_details': [
            {u'note': u'Not a real address',
             u'type': u'address',
             u'value': u'123 Example Street'},
            {u'note': u'Fake phone',
             u'type': u'cell',
             u'value': u'(123)456-7890'}],
        u'geography_id': u'ocd-division/country:us/state:id/place:boise_city',
        u'identifiers': [],
        u'name': u'City Council',
        u'posts': [],
        u'sources': [
            {u'note': u'',
             u'url': u'http://mayor.cityofboise.org/city-council/'},
            {u'note': u"Sunlight's url",
             u'url': u'https://sunfoundation.com'}]}

    params = [
        (u'contact_type', ['address', u'cell']),
        (u'contact_note', ['Not a real address', u'Fake phone']),
        (u'contact_value', ['123 Example Street', u'(123)456-7890']),
        (u'source_url', [
            'http://mayor.cityofboise.org/city-council/',
            u'https://sunfoundation.com'
            ]),
        (u'source_note', [
            '',
            u"Sunlight's url"
            ]),
        (u'geography_id', u'ocd-division/country:us/state:id/place:boise_city'),
        (u'name', u'City Council')
        ]


class UnauthorizedUserTest(TestCase):
    '''These tests are run as a user has isn't an admin and has no
    permissions to edit anything in the database.
    '''
    fixtures = ['test_auth.json']

    tearDown = staticmethod(anthropod.tests.teardown)
    maxDiff = None

    login_credentials = dict(username='user3', password='password3')

    def setUp(self):
        '''Load test fixtures and log in before running the tests.'''
        load_test_fixtures()
        self.client = Client()
        self.client.login(**self.login_credentials)
        self.db = anthropod.core.db

    def test_edit(self):
        '''This test verifies that a new person created with
        the form will get saved as the expected popolo data object.
        '''
        # Create a new organization.
        url = reverse('organization.edit')
        resp = self.client.post(url, dict(self.params))

        # Make sure the unauthorized user gets a 403 page.
        self.assertEquals(resp.status_code, 403)

    params = [
        (u'contact_type', ['address', u'cell']),
        (u'contact_note', ['Not a real address', u'Fake phone']),
        (u'contact_value', ['123 Example Street', u'(123)456-7890']),
        (u'source_url', [
            'http://mayor.cityofboise.org/city-council/',
            u'https://sunfoundation.com'
            ]),
        (u'source_note', [
            '',
            u"Sunlight's url"
            ]),
        (u'geography_id', u'ocd-division/country:us/state:id/place:boise_city'),
        (u'name', u'City Council')
        ]
