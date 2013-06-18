import re

from django.test import Client, TestCase
from django.core.urlresolvers import reverse, resolve

import anthropod.core
import anthropod.tests

from anthropod.collect.views import person

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
        ('alternate_name_note', ['first', '']),
        ('name', ['China Terrell']),
        ('contact_type', ['address', 'email', '']),
        ('gender', ['f']),
        ('image', ['']),
        ('contact_note', ['', '', '']),
        ('org_id', ['']),
        ('contact_value', ['1900 Lamont Street, NW Apt. 304 Washington, DC 20010', '1D05@anc.dc.gov', '']),
        ('source_url', ['http://anc.dc.gov/page/advisory-neighborhood-commission-1d', 'https://sunfoundation.com', '']),
        ('link_note', ['twitter', '']),
        ('alternate_name_name', ['Jim', '']),
        ('birth_date', ['']),
        ('_id', ['ocd-person/04907cda-bcaf-11e2-9f80-12313d2facc4']),
        ('link_url', ['http://twitter.com/twneale', '']),
        ('biography', ['']),
        ('source_note', ['', 'Test Url', ''])
        ]


class AuthorizedMixin(Mixin):
    '''This class defines tests that are common to admin users and
    authorized users that have explicit permissions to edit things.
    '''
    expected = {
        '_type': 'person',
        'biography': None,
        'birth_date': None,
        'contact_details': [
            {'type': 'address',
             'value': '1900 Lamont Street, NW Apt. 304 Washington, DC 20010',
             'note': None},
            {'type': 'email',
             'value': '1D05@anc.dc.gov',
             'note': None}],
        'death_date': None,
        'extras': {},
        'gender': 'f',
        'image': None,
        'links': [{u'note': u'twitter', u'url': u'http://twitter.com/twneale'}],
        'name': 'China Terrell',
        'other_names': [{'name': 'Jim', 'note': 'first'}],
        'sources': [
            {'url': 'http://anc.dc.gov/page/advisory-neighborhood-commission-1d',
             'note': None},
            {'note': 'Test Url', 'url': u'https://sunfoundation.com'}],
        'summary': None}

    def test_edit(self):
        '''This test verifies that a new person created with
        the form will get saved as the expected popolo data object.
        '''
        # Create a new person.
        url = reverse('person.edit')
        resp = self.client.post(url, dict(self.params))

        # Make sure we redirected after the save.
        self.assertEquals(resp.status_code, 302)

        # Verify that the redirect was to the org jsonview.
        location = dict(resp.items())['Location']
        location = re.sub('http://testserver', '', location)
        redirect_view = resolve(location).func
        self.assertEquals(redirect_view, person.jsonview)

        # Now verify that the saved popolo object
        # matches what we expect.
        ocd_id = re.search(r'ocd-person.+', location).group()
        ocd_id = ocd_id.rstrip('/')
        saved = self.db.people.find_one(ocd_id)
        saved.pop('_id')

        self.assertEquals(saved, self.expected)

    def test_delete(self):
        url = reverse('person.delete')
        params = [(
            '_id',
            'ocd-person/04907cda-bcaf-11e2-9f80-12313d2facc4')]

        resp = self.client.post(url, dict(params))

        # Make sure we redirected after the save.
        self.assertEquals(resp.status_code, 302)

        # Verify that the redirect was to the org listing.
        location = dict(resp.items())['Location']
        location = re.sub('http://testserver', '', location)
        redirect_view = resolve(location).func
        self.assertEquals(redirect_view, person.listing)


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
        # Create a new person.
        url = reverse('person.edit')
        resp = self.client.post(url, dict(self.params))

        # Make sure the unauthorized user gets a 403 page.
        self.assertEquals(resp.status_code, 403)

    def test_delete(self):
        # Create a new person.
        url = reverse('person.delete')
        params = [(
            '_id',
            'ocd-person/1bfc9aac-b29b-11e2-9e8b-12313d2facc4')]
        resp = self.client.post(url, dict(params))

        # Make sure we redirected after the save.
        self.assertEquals(resp.status_code, 403)
