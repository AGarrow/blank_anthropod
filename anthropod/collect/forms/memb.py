from django import forms

from .base import BaseForm


class EditForm(BaseForm):
    '''Provide a form for manual data collection of the fields
    described on the Manual-data-collection-tool page of the
    open-civic-data wiki.

    See: https://github.com/opencivicdata/opencivicdata/wiki/
    '''
    # Required fields.
    organization_id = forms.CharField()
    person_id = forms.CharField()
    role = forms.CharField(required=False)
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)

    def as_popolo(self, request):
        '''Return this form's data as a popolo person.
        '''
        obj = {}

        # Add the top-level required fields.
        for field in self:
            name = field.name
            value = self.data.get(name)
            if value:
                obj[name] = value

        # Add the contact info.
        obj['contact_details'] = self.contact(request)
        obj['sources'] = self.sources(request)

        return obj

    @classmethod
    def from_popolo(cls, obj):
        formdata = {}

        for name, field in cls.single_fields():
            if name not in obj:
                continue
            value = obj[name]
            if value:
                formdata[name] = value

        form = cls(formdata)
        form.contacts = obj.get('contact_details', [])
        form.sources = obj.get('sources', [])

        return form
