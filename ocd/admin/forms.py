import collections
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

    CONTACT_TYPE_CHOICES = _mk_choices([
        '',
        'address',
        'voice',
        'fax',
        'cell',
        'tollfree',
        'video',
        'textphone',
        'email'])

    contact_note = forms.CharField(required=False)
    contact_type = forms.ChoiceField(
        choices=CONTACT_TYPE_CHOICES, required=False)
    contact_value = forms.CharField(required=False)

    # How many times to display the contact fields.
    REPEAT_CONTACT_FIELDS = range(5)

    link_note = forms.CharField(required=False)
    link_url = forms.CharField(required=False)
    REPEAT_LINK_FIELDS = range(3)

    ALT_NAME_NOTE_CHOICES = _mk_choices(['', 'first', 'last', 'nickname'])
    alternate_name_note = forms.ChoiceField(
        choices=ALT_NAME_NOTE_CHOICES, required=False)
    alternate_name_name = forms.CharField(required=False)
    REPEAT_ALTERNATE_NAME_FIELDS = range(3)

    def __iter__(self):
        '''When displaying the form with {% for field in form %},
        only display fields that don't begin with "alternate_name",
        "contact", or "link".
        '''
        skip = ('contact', 'link', 'alternate_name')
        for field in super(PersonForm, self).__iter__():
            if not field.name.startswith(skip):
                yield field

    # Methods for converting this form's data into a popolo person object.
    def _get_zipped_field_data(self, request, prefix, fields, asdict=True):
        '''POST.getlist the values of fields prefixed with `prefix`
        and zip them together. Generate a stream of dicts.
        '''
        field_names = [prefix + field for field in fields]
        get = request.POST.getlist

        for vals in zip(*map(get, field_names)):
            # Skip emtpy form values.
            if any(vals):
                if asdict:
                    yield dict(zip(fields, vals))
                else:
                    yield vals

    def zipfields(self, request, prefix, fields, asdict=True):
        '''A more convenient wrapper for the previous function.
        '''
        data = self._get_zipped_field_data(request, prefix, fields, asdict)
        return list(data)

    def contact(self, request):
        '''Return this form's contact data as a popolo array like:
        [
            ["office", "voice" "+1-800-555-0100;ext=555"],
            ["home", "fax", "+1-800-555-0199"]
        ]
        '''
        return self.zipfields(request,
                              prefix='contact_',
                              fields=('note', 'type', 'value'),
                              asdict=False)

    def alternate_names(self, request):
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
        return self.zipfields(request,
                              prefix='alternate_name_',
                              fields=('note', 'name'))

    def links(self, request):
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
        return self.zipfields(request,
                              prefix='link_',
                              fields=('note', 'url'))

    def as_popolo(self, request):
        '''Return this form's data as a popolo person.
        '''
        person = {}

        # Add the top-level required fields.
        for name, field in self.base_fields.items():
            if field.required:
                person[name] = self.data[name]

        person['addresses'] = self.contact(request)
        person['other_names'] = self.alternate_names(request)
        person['links'] = self.links(request)

        return person

    @classmethod
    def from_popolo(cls, person):
        formdata = {}
        for name, field in cls.base_fields.items():
            if field.required:
                formdata[name] = person[name]

        form = cls(formdata)
        form.contacts = person['addresses']

        links = []
        for link in person['links']:
            links.append((link['url'], link['note']))
        form.links = links

        alternate_names = []
        for name in person['other_names']:
            alternate_names.append((name['name'], name['note']))
        form.alt_names = alternate_names
        return form

    def single_fields(self):
        for name, field in self.base_fields.items():
            if not name.startswith(('contact', 'alternate_name', 'link')):
                yield name, field






