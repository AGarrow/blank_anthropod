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

    # Methods for converting this form's data into a popolo person object.
    def _required(self):
        '''Return this form's required fields.
        '''
        return filter(lambda item: item[1].required, self.fields.items())

    def _get_zipped_field_data(self, request, prefix, fields):
        '''POST.getlist the values of fields prefixed with `prefix`
        and zip them together. Generate a stream of dicts.
        '''
        field_names = [prefix + field for field in fields]
        get = request.POST.getlist

        for vals in zip(*map(get, field_names)):
            # Skip emtpy form values.
            if any(vals):
                yield dict(zip(fields, vals))

    def zipfields(self, request, prefix, fields):
        '''A more convenient wrapper for the previous function.
        '''
        return list(self._get_zipped_field_data(request, prefix, fields))

    def contact(self, request):
        '''Return this form's contact data as a popolo array like:
        [
            {
                "type": "office",
                "voice": "+1-800-555-0100;ext=555",
                "fax": "+1-800-555-0199"
            }
        ]
        '''
        items = self.zipfields(request,
                               prefix='contact_',
                               fields=('type', 'field', 'value'))

        # Group them by popolo type.
        grouped = collections.defaultdict(dict)
        for item in items:
            grouped[item['type']][item['field']] = item['value']

        # Add the popolo type to each dictionary.
        result = []
        for type_, data in grouped.items():
            data['type'] = type_
            result.append(data)

        return result

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
        for name, field in self._required():
            person[name] = self.data[name]

        person['addresses'] = self.contact(request)
        person['other_names'] = self.alternate_names(request)
        person['links'] = self.links(request)

        return person










