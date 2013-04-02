from django.utils import unittest
from django.test import Client
from django.core.urlresolvers import reverse

import anthropod.tests
from anthropod.core import db
from ..fixtures import load as load_people
from ...organization.fixtures import load as load_orgs


class CreatePersonTest(unittest.TestCase):
    '''This test verifies that a new person created with
    the form will get saved as the expected popolo data object.
    u'''
    tearDown = staticmethod(anthropod.tests.teardown)
    maxDiff = None

    def setUp(self):
        '''Start with an empty database.'''
        self.client = Client()
        load_orgs()

    def test_person_form(self):
        '''Submit the person form with valid data. Ensure that
        the form validates the data and saves is as the expected
        popolo equivalent in mongo.
        u'''
        # Create a new person.
        url = reverse('person.create')

        # Get the associated org.
        org = db.organizations.find_one()

        # Keep the org id as a string for convenience.
        self.params += [('organization_id', str(org['_id']))]
        self.expected['organization_id'] = org['_id']

        resp = self.client.post(url, dict(self.params))

        # A successful post and form validation should
        # trigger a redirect to the person's page.
        self.assertEquals(resp.status_code, 302)

        # Now verify that the saved popolo object
        # matches what we expect.
        saved = db.people.find_one()
        saved.pop('_id')
        self.assertEquals(saved, self.expected)

    expected = {
        u'addresses': [
            [u'voice', u'1-234-567-8901', u'work'],
            [u'tollfree', u'1-800-555-5555', u'home'],
            [u'address', u'123 Dupont Circle', u'Work']],
        u'geography_id': u'ocd:location:country-us:state-texas:city-plano',
        u'links': [
            {u'note': u'Twitter',
             u'url': u'http://twitter.com/twneale'},
            {u'note': u'Facebook',
             u'url': u'http://facebook.com/thom'}],
        u'name': u'Thom Neale',
        u'other_names': [
            {u'name': u'Thommy', u'note': u'first'},
            {u'name': u'Fool', u'note': u'first'},
            {u'name': u"O'Neil", u'note': u'last'}],
        u'position': u'Nerd',
        u'gender': u'f',
        u'source_url': u'http://www.thomneale.com'}

    params = [
        (u'alternate_name_name',
         [u'Thommy', u'Fool', "O'Neil"]),

        (u'alternate_name_note',
         [u'first', u'first', u'last', u'nickname']),

        (u'name', u'Thom Neale'),
        (u'gender', u'f'),
        (u'image', u''),

        (u'contact_type', [u'voice', u'tollfree', u'address']),
        (u'contact_note', [u'work', u'home', u'Work']),
        (u'contact_value',
         [u'1-234-567-8901', u'1-800-555-5555', u'123 Dupont Circle']),

        (u'source_url', u'http://www.thomneale.com'),
        (u'geography_id', u'ocd:location:country-us:state-texas:city-plano'),

        (u'link_note', [u'Twitter', u'Facebook']),

        (u'link_url',
         [u'http://twitter.com/twneale', u'http://facebook.com/thom']),

        (u'party', u''),
        (u'birth_date', u''),
        (u'position', u'Nerd'),
        (u'biography', u'')]


class EditPersonTest(unittest.TestCase):
    u'''This test verifies that posting to the edit form changes the
    saved popolo object in the way we expect.
    u'''
    tearDown = staticmethod(anthropod.tests.teardown)
    maxDiff = None

    def setUp(self):
        self.client = Client()
        self.db = db
        load_orgs()
        load_people()

    def test_person_form(self):
        u'''Submit the person form with valid data. Ensure that
        the form validates the data and modifies the "Thom" fixture
        in the expected way, here mangling the letting of the values.
        u'''

        # Get the Thom fixture.
        thom = db.people.find_one(dict(position='Nerd'))

        # Get the associated org.
        org = db.organizations.find_one()

        # Construct the edit url.
        url = reverse('person.edit', args=(str(thom['_id']),))

        # Keep the org id as a string for convenience.
        self.params += [('organization_id', str(org['_id']))]
        self.expected['organization_id'] = org['_id']

        # Post the edited params.
        resp = self.client.post(url, dict(self.params))

        # A successful post and form validation should
        # trigger a redirect to Thom's detail page.
        self.assertEquals(resp.status_code, 302)

        # Now verify that the saved popolo object
        # matches what we expect.
        saved = db.people.find_one()
        saved.pop('_id')
        self.assertEquals(saved, self.expected)

    expected = {
        u'addresses': [
            [u'voice', u'1-234-567-89o1', u'work'],
            [u'tollfree', u'1-8oo-555-5555', u'hom3'],
            [u'address', u'123 Dupont Circl3', u'Work']],
        u'geography_id': u'ocd:location:country-us:state-texas:city-plano',
        u'links': [
            {u'note': u'Twitt3r',
             u'url': u'http://twitt3r.com/twn3al3'},
            {u'note': u'Fac3book',
             u'url': u'http://fac3book.com/thom'}],
        u'name': u'Thom N3al3',
        u'party': u't3st',
        u'gender': u'm',
        u'other_names': [
            {u'name': u'Thommy', u'note': u'first'},
            {u'name': u"O'N3il", u'note': u'last'},
            {u'name': u"thommy boy", u'note': u'nickname'}],
        u'position': u'N3rd',
        u'source_url': u'http://www.thomn3al3.com'}

    params = [
        (u'alternate_name_name',
         [u'Thommy', u"O'N3il", u'thommy boy']),

        (u'alternate_name_note',
         [u'first', u'last', u'nickname']),

        (u'name', u'Thom N3al3'),
        (u'gender', u'm'),
        (u'image', u''),

        (u'source_url', u'http://www.thomn3al3.com'),
        (u'geography_id', u'ocd:location:country-us:state-texas:city-plano'),

        (u'link_note', [u'Twitt3r', u'Fac3book']),

        (u'link_url',
         [u'http://twitt3r.com/twn3al3', u'http://fac3book.com/thom']),

        (u'party', u't3st'),
        (u'birth_date', u''),
        (u'position', u'N3rd'),
        (u'biography', u''),

        (u'contact_note', [u'work', u'hom3', u'Work']),
        (u'contact_type', [u'voice', u'tollfree', u'address']),
        (u'contact_value',
         [u'1-234-567-89o1', u'1-8oo-555-5555', u'123 Dupont Circl3'])]
