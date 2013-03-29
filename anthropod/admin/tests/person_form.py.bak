from django.utils import unittest
from django.test import Client
from django.core.urlresolvers import reverse

import ocd.core
import ocd.tests
import ocd.fixtures.people


class CreatePersonTest(unittest.TestCase):
    '''This test verifies that a new person created with
    the form will get saved as the expected popolo data object.
    '''
    tearDown = staticmethod(ocd.tests.teardown)
    maxDiff = None

    def setUp(self):
        '''Start with an empty database.'''
        self.client = Client()
        self.db = ocd.core.db

    def test_person_form(self):
        '''Submit the person form with valid data. Ensure that
        the form validates the data and saves is as the expected
        popolo equivalent in mongo.
        '''
        # Create a new person.
        url = reverse('person.create')
        resp = self.client.post(url, dict(self.params))

        # A successful post and form validation should
        # trigger a redirect to the person's page.
        self.assertEquals(resp.status_code, 302)

        # Now verify that the saved popolo object
        # matches what we expect.
        saved = self.db.people.find_one()
        saved.pop('_id')
        self.assertEquals(saved, self.expected)

    expected = {
        'addresses': [
            ['work', 'voice', '1-234-567-8901'],
            ['home', 'tollfree', '1-800-555-5555'],
            ['Work', 'address', '123 Dupont Circle']],
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
            {'name': "O'Neil", 'note': 'last'}],
        'position': 'Nerd',
        'gender': 'f',
        'source_url': 'http://www.thomneale.com'}

    params = [
        ('alternate_name_name',
         ['Thommy', 'Fool', "O'Neil"]),

        ('alternate_name_note',
         ['first', 'first', 'last', 'nickname']),

        ('name', 'Thom Neale'),
        ('contact_type', ['voice', 'tollfree', 'address']),
        ('gender', 'f'),
        ('image', ''),

        ('contact_note',
         ['work', 'home', 'Work']),

        ('source_url', 'http://www.thomneale.com'),
        ('geography_id', 'ocd:location:country-us:state-texas:city-plano'),

        ('link_note', ['Twitter', 'Facebook']),

        ('link_url',
         ['http://twitter.com/twneale', 'http://facebook.com/thom']),

        ('party', ''),
        ('birth_date', ''),
        ('position', 'Nerd'),
        ('biography', ''),

        ('contact_value',
         ['1-234-567-8901', '1-800-555-5555', '123 Dupont Circle'])]


class EditPersonTest(unittest.TestCase):
    '''This test verifies that posting to the edit form changes the
    saved popolo object in the way we expect.
    '''
    tearDown = staticmethod(ocd.tests.teardown)
    maxDiff = None

    def setUp(self):
        self.client = Client()
        self.db = ocd.core.db
        ocd.fixtures.people.load()

    def test_person_form(self):
        '''Submit the person form with valid data. Ensure that
        the form validates the data and modifies the "Thom" fixture
        in the expected way, here mangling the letting of the values.
        '''

        # Get the Thom fixture.
        thom = self.db.people.find_one(dict(position='Nerd'))

        # Construct its edit url.
        url = reverse('person.edit', args=(str(thom['_id']),))

        # Post the edited params.
        resp = self.client.post(url, dict(self.params))

        # A successful post and form validation should
        # trigger a redirect to Thom's detail page.
        self.assertEquals(resp.status_code, 302)

        # Now verify that the saved popolo object
        # matches what we expect.
        saved = self.db.people.find_one()
        saved.pop('_id')
        self.assertEquals(saved, self.expected)

    expected = {
        'addresses': [
            ['work', 'voice', '1-234-567-89o1'],
            ['hom3', 'tollfree', '1-8oo-555-5555'],
            ['Work', 'address', '123 Dupont Circl3']],
        'geography_id': 'ocd:location:country-us:state-texas:city-plano',
        'links': [
            {'note': 'Twitt3r',
             'url': 'http://twitt3r.com/twn3al3'},
            {'note': 'Fac3book',
             'url': 'http://fac3book.com/thom'}],
        'name': 'Thom N3al3',
        'party': 't3st',
        'gender': 'm',
        'other_names': [
            {'name': 'Thommy', 'note': 'first'},
            {'name': "O'N3il", 'note': 'last'},
            {'name': "thommy boy", 'note': 'nickname'}],
        'position': 'N3rd',
        'source_url': 'http://www.thomn3al3.com'}

    params = [
        ('alternate_name_name',
         ['Thommy', "O'N3il", 'thommy boy']),

        ('alternate_name_note',
         ['first', 'last', 'nickname']),

        ('name', 'Thom N3al3'),
        ('contact_type', ['voice', 'tollfree', 'address']),
        ('gender', 'm'),
        ('image', ''),

        ('contact_note',
         ['work', 'hom3', 'Work']),

        ('source_url', 'http://www.thomn3al3.com'),
        ('geography_id', 'ocd:location:country-us:state-texas:city-plano'),

        ('link_note', ['Twitt3r', 'Fac3book']),

        ('link_url',
         ['http://twitt3r.com/twn3al3', 'http://fac3book.com/thom']),

        ('party', 't3st'),
        ('birth_date', ''),
        ('position', 'N3rd'),
        ('biography', ''),

        ('contact_value',
         ['1-234-567-89o1', '1-8oo-555-5555', '123 Dupont Circl3'])]
