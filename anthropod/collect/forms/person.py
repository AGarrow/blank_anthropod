from operator import itemgetter

from django import forms

from .base import BaseForm


first = itemgetter(0)
second = itemgetter(1)


def _mk_choices(iterable):
    return zip(iterable, iterable)


class EditForm(BaseForm):
    '''Provide a form for manual data collection of the fields
    described on the Manual-data-collection-tool page of the
    open-civic-data wiki.

    See: https://github.com/opencivicdata/opencivicdata/wiki/
    '''
    # Required fields.
    name = forms.CharField()

    # Optional fields.
    gender = forms.ChoiceField(
        choices=[('', ''), ('f', 'Female'), ('m', 'Male')],
        required=False)
    # party = forms.CharField(required=False)
    birth_date = forms.DateField(required=False)
    image = forms.URLField(required=False)
    biography = forms.CharField(widget=forms.Textarea, required=False)

    link_note = forms.CharField(required=False)
    link_url = forms.CharField(required=False)

    ALT_NAME_NOTE_CHOICES = _mk_choices(['', 'first', 'last', 'nickname'])
    alternate_name_note = forms.ChoiceField(
        choices=ALT_NAME_NOTE_CHOICES, required=False)
    alternate_name_name = forms.CharField(required=False)

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
        obj = {}

        # Add the top-level required fields.
        for name, field in self.single_fields():
            value = self.data[name]
            if value:
                obj[name] = self.data[name]

        obj['contact_details'] = self.contact(request)
        obj['other_names'] = self.alternate_names(request)
        obj['links'] = self.links(request)
        obj['sources'] = self.sources(request)

        return obj

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
        form.contacts = person.get('contact_details')

        links = []
        for link in person['links']:
            links.append((link['url'], link['note']))
        form.links = links

        alternate_names = []
        for name in person['other_names']:
            alternate_names.append((name['name'], name['note']))
        form.alt_names = alternate_names
        form.sources = person.get('sources')
        return form
