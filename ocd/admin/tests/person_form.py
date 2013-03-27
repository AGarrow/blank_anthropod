from django.utils import unittest
from django.test import Client
from django.core.urlresolvers import reverse

import ocd.core
import ocd.tests
import ocd.fixtures.people


class BaseTestCase(unittest.TestCase):

    tearDown = staticmethod(ocd.tests.teardown)

    def setUp(self):
        self.client = Client()
        self.db = ocd.core.db
        ocd.fixtures.people.load()

    def test_person_form(self):
        '''Submit the person form with valid data. Ensure that
        the form validates the data and saves is as the expected
        popolo equivalent in mongo.
        '''
        params = [
            ('alternate_name_name', "O'Neil"),
            ('alternate_name_note', 'last'),
            ('name', 'Thom Neale'),
            ('contact_type', 'home'),
            ('gender', 'f'),
            ('image', ''),
            ('contact_field', 'tollfree'),
            ('source_url', 'http://www.thomneale.com'),
            ('geography_id', 'ocd:location:country-us:state-texas:city-plano'),
            ('link_note', ''),
            ('party', ''),
            ('birth_date', ''),
            ('position', 'Nerd'),
            ('link_url', ''),
            ('biography', ''),
            ('contact_value', '1-800-555-5555')]

        url = reverse('person.create')
        resp = self.client.post(url, dict(params))

        # A successful post and form validation should
        # trigger a redirect to the person's page.
        self.assertEquals(resp.status_code, 302)

        # Now verify that the saved popolo object
        # matches what we expect.
        expected = {
            'addresses': [
                {'type': 'work',
                 'voice': '1-234-567-8901'},
                {'tollfree':
                 '1-800-555-5555', 'type': 'home'},
                {'address':
                 '123 Dupont Circle', 'type': 'Work'}],
            'geography_id': 'ocd:location:country-us:state-texas:city-plano',
            'links': [
                {'note': 'Twitter',
                 'url': 'http://twitter.com/twneale'},
                {'note': 'Facebook',
                 'url': 'http://facebook.com/thom'}],
            'name': 'Thom Neale',
            'other_names': [
                {'name': 'Thommy', 'note': 'first'},
                {'name': 'Fool', 'note': 'first'},
                {'name': u"O'Neil", 'note': 'last'}],
            'position': 'Nerd',
            'source_url': 'http://www.thomneale.com'}

        saved = self.db.people.find_one()
        saved.pop('_id')
        self.assertEquals(saved, expected)
