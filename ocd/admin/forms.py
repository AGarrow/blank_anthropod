import re
import collections
from itertools import groupby
from operator import itemgetter

from django import forms


first = itemgetter(0)
second = itemgetter(1)

GEO_CHOICES = [
    ('', ''),
    ('ocd:location:country-us:state-texas:city-plano',
     'City of Plano, TX'),
    ('ocd:location:country-us:state-idaho:city-boise',
     'City of Boise, ID'),
    ('ocd:location:country-us:state-nevada:city-reno',
     'City of Reno, NV'),
    ]


def _mk_choices(iterable):
    return zip(iterable, iterable)


class PersonForm(forms.Form):
    '''Provide a form for manual data collection of the fields
    described on the Manual-data-collection-tool page of the
    open-civic-data wiki.

    See: https://github.com/opencivicdata/opencivicdata/wiki/
    '''
    # Required fields.
    name = forms.CharField()
    geography_id = forms.ChoiceField(choices=GEO_CHOICES)
    position = forms.CharField()
    source_url = forms.URLField()

    # Optional fields.
    gender = forms.ChoiceField(choices=[('f', 'Female'), ('m', 'Male')],
                               required=False)
    party = forms.CharField(required=False)
    birth_date = forms.DateField(required=False)
    image = forms.URLField(required=False)
    biography = forms.CharField(widget=forms.Textarea, required=False)

    # # Alternate name fields.
    # ALT_NAME_TYPE_CHOICES = _mk_choices(['', 'first', 'last', 'nickname'])

    # alternate_name_note_1 = forms.ChoiceField(
    #     choices=ALT_NAME_TYPE_CHOICES, required=False)
    # alternate_name_name_1 = forms.CharField(required=False)

    # alternate_name_note_2 = forms.ChoiceField(
    #     choices=ALT_NAME_TYPE_CHOICES, required=False)
    # alternate_name_name_2 = forms.CharField(required=False)

    # alternate_name_note_3 = forms.ChoiceField(
    #     choices=ALT_NAME_TYPE_CHOICES, required=False)
    # alternate_name_name_3 = forms.CharField(required=False)

    # link_url_1 = forms.CharField(required=False)
    # link_note_1 = forms.CharField(required=False)

    # link_url_2 = forms.CharField(required=False)
    # link_note_2 = forms.CharField(required=False)

    # link_url_3 = forms.CharField(required=False)
    # link_note_3 = forms.CharField(required=False)

    # link_url_4 = forms.CharField(required=False)
    # link_note_4 = forms.CharField(required=False)

    # link_url_5 = forms.CharField(required=False)
    # link_note_5 = forms.CharField(required=False)

    # CONTACT_TYPE_CHOICES = _mk_choices([
    #     '',
    #     'address',
    #     'voice',
    #     'fax',
    #     'cell',
    #     'tollfree',
    #     'video',
    #     'textphone',
    #     'email'])

    # # Contact fields with note.
    # contact_type_1 = forms.ChoiceField(
    #     choices=CONTACT_TYPE_CHOICES, required=False)
    # contact_note_1 = forms.CharField(required=False)
    # contact_value_1 = forms.CharField(required=False)

    # contact_type_2 = forms.ChoiceField(
    #     choices=CONTACT_TYPE_CHOICES, required=False)
    # contact_note_2 = forms.CharField(required=False)
    # contact_value_2 = forms.CharField(required=False)

    # contact_type_3 = forms.ChoiceField(
    #     choices=CONTACT_TYPE_CHOICES, required=False)
    # contact_note_3 = forms.CharField(required=False)
    # contact_value_3 = forms.CharField(required=False)

    # contact_type_4 = forms.ChoiceField(
    #     choices=CONTACT_TYPE_CHOICES, required=False)
    # contact_note_4 = forms.CharField(required=False)
    # contact_value_4 = forms.CharField(required=False)

    # contact_type_5 = forms.ChoiceField(
    #     choices=CONTACT_TYPE_CHOICES, required=False)
    # contact_note_5 = forms.CharField(required=False)
    # contact_value_5 = forms.CharField(required=False)

    # Methods for converting this form's data into a popolo person object.
    def _required(self):
        '''Return this form's required fields.
        '''
        return filter(lambda item: item[1].required, self.fields.items())

    def _optional(self):
        '''Return this form's optional fields.
        '''
        return filter(lambda item: not item[1].required, self.fields.items())

    def _optional_keys(self):
        '''Return the field names of this form's optional fields.
        '''
        return map(first, self._optional())

    def _group_fields_by_prefix(self):
        '''Group the contact_type_1, contact_type_2 field names together.
        '''
        rgx = r'(contact|link|alternate_name)'
        groupable = [(re.match(rgx, key), key) for key in self._optional_keys()]
        groupable = filter(first, groupable)
        groupable = [(match.group(), key) for (match, key) in groupable]
        result = collections.defaultdict(list)
        for prefix, key in groupable:
            result[prefix].append(key)
        return result

    def _group_fields_by_index(self, prefix):
        '''Yield tuples like:
            ('contact_type_1', 'contact_note_1', 'contact_value_1')
            ('contact_type_2', 'contact_note_2', 'contact_value_2')
            ('contact_type_3', 'contact_note_3', 'contact_value_3')
            ('contact_type_4', 'contact_note_4', 'contact_value_4')
            ('contact_type_5', 'contact_note_5', 'contact_value_5')
        '''
        keys = self._group_fields_by_prefix()[prefix]
        search = re.search
        groupable = [(search('\d+', key), key) for key in keys]
        groupable = filter(first, groupable)
        groupable = [(match.group(), key) for (match, key) in groupable]
        grouped = groupby(groupable, first)
        for index, keys in grouped:
            yield tuple(map(second, keys))

    def _tuple_group_to_dict(self, tpl):
        '''Converts: ('contact_type_5', 'contact_note_5')
           Into: {'type': somedata1, 'note': somedata2}
        '''
        result = {}
        for fieldname in tpl:
            key = fieldname.split('_')[-2]
            result[key] = self.data[fieldname]
        return result

    def contact(self):
        '''Return this form's contact data as a popolo array like:
        [
            {
                "type": "office",
                "voice": "+1-800-555-0100;ext=555",
                "fax": "+1-800-555-0199"
            }
        ]
        '''
        data = map(
            self._tuple_group_to_dict,
            self._group_fields_by_index('contact'))

        result = collections.defaultdict(dict)
        for item in data:
            # Skip empty form fields.
            if not item['type']:
                continue
            result[item['note']][item['type']] = item['value']
        return result

    def _filterfalse(self, dict_list):
        '''Return only the dicts in a dict list that have non-false values.
        '''
        return list(obj for obj in dict_list if any(obj.values()))

    def alternate_names(self):
        '''
        Return this form's alternate names as a popolo array like:
        [
            {
                "name": "Bob's Diner",
                "start_date": "1950-01-01",
                "end_date": "1954-12-31"
            },
            {
                "name": "Joe's Diner",
                "start_date": "1955-01-01"
            }
        ]
        '''
        return self._filterfalse(map(
            self._tuple_group_to_dict,
            self._group_fields_by_index('alternate_name')))

    def links(self):
        '''Return this form's links as a popolo array like:
        [
            {
              "url": "http://twitter.com/ev",
              "note": "Twitter account"
            },
            {
              "url": "http://en.wikipedia.org/wiki/John_Q._Public",
              "note": "Wikipedia page"
            }
        ]
        '''
        return self._filterfalse(map(
            self._tuple_group_to_dict,
            self._group_fields_by_index('link')))

    def as_popolo(self):
        '''Return this form's data as a popolo person.
        '''
        person = {}

        # Add the top-level required fields.
        for name, field in self._required():
            person[name] = self.data[name]

        person['addresses'] = dict(self.contact())
        person['other_names'] = self.alternate_names()
        person['links'] = self.links()

        return person










