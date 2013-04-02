from operator import itemgetter

from django import forms
from anthropod.core import db

GEO_CHOICES = [('', '')] + [(div['_id'], div['name']) for div in db.divisions.find()]


class EditForm(forms.Form):
    '''Provide a form for manual data collection of the fields
    described on the Manual-data-collection-tool page of the
    open-civic-data wiki.

    See: https://github.com/opencivicdata/opencivicdata/wiki/
    '''
    # Required fields.
    name = forms.CharField()
    geography_id = forms.ChoiceField(choices=GEO_CHOICES)
    source_url = forms.URLField()

    def as_popolo(self, request):
        '''Return this form's data as a popolo person.
        '''
        obj = {}

        # Add the top-level required fields.
        for name, field in self.base_fields.items():
            value = self.data[name]
            if value:
                obj[name] = self.data[name]

        return obj

    @classmethod
    def from_popolo(cls, obj):
        formdata = {}

        for name, field in cls.base_fields.items():
            if name not in obj:
                continue
            value = obj[name]
            if value:
                formdata[name] = value

        return cls(formdata)



