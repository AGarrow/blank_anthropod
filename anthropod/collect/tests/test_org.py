import re

from django.test import Client, TestCase
from django.core.urlresolvers import reverse, resolve

import anthropod.core
import anthropod.tests

from anthropod.collect.views import organization

from .fixtures import load_test_fixtures


class Mixin(object):
    '''This class provides names and data common to all the tests
    in this module.
    '''
    fixtures = ['test_auth.json']
    tearDown = staticmethod(anthropod.tests.teardown)
    maxDiff = None

    def setUp(self):
        '''Load test fixtures and log in before running the tests.'''
        load_test_fixtures()
        self.client = Client()
        self.client.login(**self.login_credentials)
        self.db = anthropod.core.db

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


class AuthorizedMixin(Mixin):
    '''This class defines tests that are common to admin users and
    authorized users that have explicit permissions to edit things.
    '''
    expected = {
        '_type': 'organization',
        'classification': None,
        'contact_details': [
            {'note': 'Not a real address',
             'type': 'address',
             'value': '123 Example Street'},
            {'note': 'Fake phone',
             'type': 'cell',
             'value': '(123)456-7890'}],
        'dissolution_date': None,
        'founding_date': None,
        'geography_id': 'ocd-division/country:us/state:id/place:boise_city',
        'identifiers': [],
        'name': 'City Council',
        'other_names': [],
        'parent_id': None,
        'posts': [],
        'sources': [
            {'url': 'http://mayor.cityofboise.org/city-council/',
             'note': None},
            {'note': "Sunlight's url",
             'url': 'https://sunfoundation.com'}]
        }


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
        self.assertEquals(redirect_view, organization.jsonview)

        # Now verify that the saved popolo object
        # matches what we expect.
        ocd_id = re.search(r'ocd-organization.+', location).group()
        ocd_id = ocd_id.rstrip('/')
        saved = self.db.organizations.find_one(ocd_id)
        saved.pop('_id')

        self.assertEquals(saved, self.expected)

    def test_delete(self):
        # Create a new organization.
        url = reverse('organization.delete')
        params = [(
            '_id',
            'ocd-organization/1bfc9aac-b29b-11e2-9e8b-12313d2facc4')]
        resp = self.client.post(url, dict(params))

        # Make sure we redirected after the save.
        self.assertEquals(resp.status_code, 302)

        # Verify that the redirect was to the org listing.
        location = dict(resp.items())['Location']
        location = re.sub('http://testserver', '', location)
        redirect_view = resolve(location).func
        self.assertEquals(redirect_view, organization.listing)


class AdminUserTest(AuthorizedMixin, TestCase):
    '''The tests on this class run as a user with admin priviliges.
    '''
    login_credentials = dict(username='user1', password='password1')


class AuthorizedUserTest(AuthorizedMixin, TestCase):
    '''These tests are run as a user isn't an admin but has
    permissions to edit all the objects in the database.
    '''
    login_credentials = dict(username='user2', password='password2')


class UnauthorizedUserTest(Mixin, TestCase):
    '''These tests are run as a user has isn't an admin and has no
    permissions to edit anything in the database.
    '''
    login_credentials = dict(username='user3', password='password3')

    def test_edit(self):
        '''This test verifies that a new person created with
        the form will get saved as the expected popolo data object.
        '''
        # Create a new organization.
        url = reverse('organization.edit')
        resp = self.client.post(url, dict(self.params))

        # Make sure the unauthorized user gets a 403 page.
        self.assertEquals(resp.status_code, 403)

    def test_delete(self):
        # Create a new organization.
        url = reverse('organization.delete')
        params = [(
            '_id',
            'ocd-organization/1bfc9aac-b29b-11e2-9e8b-12313d2facc4')]
        resp = self.client.post(url, dict(params))

        # Make sure we redirected after the save.
        self.assertEquals(resp.status_code, 403)
