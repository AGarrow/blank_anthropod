import re

from django.test import Client, TestCase
from django.core.urlresolvers import reverse, resolve

import anthropod.core
import anthropod.tests

from anthropod.collect.views import membership, org_memb

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
        ('source_note', ['Cow', '']),
        ('end_date', ['']),
        ('contact_type', ['tollfree', 'textphone', '']),
        ('contact_note', ['note1', 'None', '']),
        ('contact_value', ['1234', 'my textphone', '']),
        ('source_url', ['http://www.thomneale.com', '']),
        ('organization_id', ['ocd-organization/1bfc9aac-b29b-11e2-9e8b-12313d2facc4']),
        ('role', ['1D05']),
        ('person_id', ['ocd-person/04907cda-bcaf-11e2-9f80-12313d2facc4']),
        ('_id', 'ocd-membership/1bfc9aac-b29b-11e2-9e8b-12313d2facc4'),
        ('start_date', ['']),
        ]


class AuthorizedMixin(Mixin):
    '''This class defines tests that are common to admin users and
    authorized users that have explicit permissions to edit things.
    '''
    expected = {
        '_type': 'membership',
        'contact_details': [
            {'note': 'note1',
             'type': 'tollfree',
             'value': '1234'},
            {'note': 'None',
             'type': 'textphone',
             'value': 'my textphone'}],
        'end_date': None,
        'organization_id': u'ocd-organization/1bfc9aac-b29b-11e2-9e8b-12313d2facc4',
        'person_id': u'ocd-person/04907cda-bcaf-11e2-9f80-12313d2facc4',
        'post_id': None,
        'role': u'1D05',
        'sources': [
            {'note': 'Cow',
             'url': 'http://www.thomneale.com'}],
        'start_date': None}

    def test_edit(self):
        '''This test verifies that a new membership edited with
        the form will be saved as the expected popolo data object.
        '''
        # Create a new membership.
        url = reverse('memb.edit')
        resp = self.client.post(url, dict(self.params))

        # Make sure we redirected after the save.
        self.assertEquals(resp.status_code, 302)

        # Verify that the redirect was to the org jsonview.
        location = dict(resp.items())['Location']
        location = re.sub('http://testserver', '', location)
        redirect_view = resolve(location).func
        self.assertEquals(redirect_view, membership.jsonview)

        # Now verify that the saved popolo object
        # matches what we expect.
        ocd_id = re.search(r'jsonview/(.+)', location).group(1)
        saved = self.db.memberships.find_one(ocd_id)
        saved.pop('_id')

        self.assertEquals(saved, self.expected)

    def test_delete(self):
        url = reverse('memb.delete')
        params = [(
            '_id',
            'ocd-membership/1bfc9aac-b29b-11e2-9e8b-12313d2facc4')]

        # Get the object.
        obj = self.db.memberships.find_one(dict(params))

        # Delete it through the website.
        resp = self.client.post(url, dict(params))

        # Make sure we redirected after the save.
        self.assertEquals(resp.status_code, 302)

        # Verify that the redirect was to the org listing.
        kwargs = dict(_id=obj.person().id)
        location = reverse('org.memb.listing', kwargs=kwargs)
        redirect_view = resolve(location).func
        self.assertEquals(redirect_view, org_memb.listing)


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
        '''This test verifies that a membership edited through
        the form will be saved as the expected popolo data object.
        '''
        # Create a new membership.
        url = reverse('memb.edit')
        resp = self.client.post(url, dict(self.params))

        # Make sure the unauthorized user gets a 403 page.
        self.assertEquals(resp.status_code, 403)

    def test_delete(self):
        # Create a new membership.
        url = reverse('memb.delete')
        params = [(
            '_id',
            'ocd-membership/1bfc9aac-b29b-11e2-9e8b-12313d2facc4')]
        resp = self.client.post(url, dict(params))

        # Make sure we redirected after the save.
        self.assertEquals(resp.status_code, 403)
