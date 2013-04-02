from django.utils import unittest
from django.test import Client
from django.core.urlresolvers import reverse

import anthropod.core
import anthropod.tests
from ..fixtures import load as load_fixtures


class CreateObjTest(unittest.TestCase):
    '''This test verifies that a new person created with
    the form will get saved as the expected popolo data object.
    '''
    tearDown = staticmethod(anthropod.tests.teardown)
    maxDiff = None

    def setUp(self):
        '''Start with an empty database.'''
        self.client = Client()
        self.db = anthropod.core.db

    def test_form(self):
        '''Submit the organization form with valid data. Ensure that
        the form validates the data and saves is as the expected
        popolo equivalent in mongo.
        '''
        # Create a new organization.
        url = reverse('organization.create')
        resp = self.client.post(url, dict(self.params))

        # A successful post and form validation should
        # trigger a redirect to the person's page.
        self.assertEquals(resp.status_code, 302)

        # Now verify that the saved popolo object
        # matches what we expect.
        saved = self.db.organizations.find_one()
        saved.pop('_id')
        self.assertEquals(saved, self.expected)

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


class EditTest(unittest.TestCase):
    '''This test verifies that posting to the edit form changes the
    saved popolo object in the way we expect.
    '''
    tearDown = staticmethod(anthropod.tests.teardown)
    maxDiff = None

    def setUp(self):
        self.client = Client()
        self.db = anthropod.core.db
        load_fixtures()

    def test_form(self):
        '''Submit the organization form with valid data. Ensure that
        the form validates the data and modifies the fixture
        in the expected way, here mangling the lettering of the values.
        '''

        # Get the fixture.
        obj = self.db.organizations.find_one(dict(name='Boise City Council'))

        # Construct its edit url.
        url = reverse('organization.edit', args=(str(obj['_id']),))

        # Post the edited params.
        resp = self.client.post(url, dict(self.params))

        # A successful post and form validation should
        # trigger a redirect to ibj's detail page.
        self.assertEquals(resp.status_code, 302)

        # Now verify that the saved popolo object
        # matches what we expect.
        saved = self.db.organizations.find_one()
        saved.pop('_id')
        self.assertEquals(saved, self.expected)

    expected = {
        'name': 'C1ty C0unc1l',
        'geography_id': 'ocd:location:country-us:state-idaho:city-boise',
        'source_url': 'http://may0r.c1ty0fb01se.org/c1ty-c0unc1l/'
    }

    params = [
        ('name', 'C1ty C0unc1l'),
        ('geography_id', 'ocd:location:country-us:state-idaho:city-boise'),
        ('source_url', 'http://may0r.c1ty0fb01se.org/c1ty-c0unc1l/'),
    ]
