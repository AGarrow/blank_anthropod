from operator import itemgetter

from bson.objectid import ObjectId
from django import forms

from anthropod.core import db


first = itemgetter(0)
second = itemgetter(1)

GEO_CHOICES = [
    ('', ''),
    ('ocd:location:country-us:state-texas:city-plano',
     'City of Plano, TX'),
    ('ocd:location:country-us:state-idaho:city-boise',
     'City of Boise, ID'),
    ('ocd:location:country-us:state-nevada:city-reno',
     'City of Reno, NV')]


def _mk_choices(iterable):
    return zip(iterable, iterable)


class EditForm(forms.Form):
    '''Provide a form for manual data collection of the fields
    described on the Manual-data-collection-tool page of the
    open-civic-data wiki.

    See: https://github.com/opencivicdata/opencivicdata/wiki/
    '''
    # Required fields.
    organization_id = forms.ChoiceField(choices=[])
    name = forms.CharField()
    geography_id = forms.ChoiceField(choices=GEO_CHOICES)
    position = forms.CharField()
    source_url = forms.URLField()

    # Optional fields.
    gender = forms.ChoiceField(
        choices=[('', ''), ('f', 'Female'), ('m', 'Male')],
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
        for field in super(EditForm, self).__iter__():
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
        '''Return this form's contact data as a list of
        (type, value, note) 3-tuples like ('voice', '12344567', 'home').
        '''
        return self.zipfields(request,
                              prefix='contact_',
                              fields=('type', 'value', 'note'),
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
        for name, field in self.single_fields():
            value = self.data[name]
            if value:
                person[name] = self.data[name]

        person['addresses'] = self.contact(request)
        person['other_names'] = self.alternate_names(request)
        person['links'] = self.links(request)

        person['organization_id'] = ObjectId(person['organization_id'])

        return person

    @classmethod
    def from_popolo(cls, person):
        formdata = {}

        for name, field in cls.single_fields():
            if name not in person:
                continue
            value = person[name]
            if value:
                formdata[name] = value

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

    @classmethod
    def single_fields(cls):
        for name, field in cls.base_fields.items():
            if not name.startswith(('contact', 'alternate_name', 'link')):
                yield name, field


def getform():
    '''This will have the same problem of hitting mongo
    for the contents of the dropdown list.
    '''
    ORG_CHOICES = [('', '')]
    for org in db.organizations.find():
        ORG_CHOICES.append((org['_id'], org['name']))

    attrs = dict(
        organization_id=forms.ChoiceField(choices=ORG_CHOICES),
        geography_id=forms.ChoiceField(choices=GEO_CHOICES))

    cls = type('EditForm', (EditForm,), attrs)

    return cls
