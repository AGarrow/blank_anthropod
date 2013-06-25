from django import forms
from django.utils.safestring import SafeText

from anthropod.core import db
from .base import BaseForm, mk_choices


def _mk_choices(iterable):
    return zip(iterable, iterable)


class EditForm(BaseForm):
    '''Provide a form for manual data collection of the fields
    described on the Manual-data-collection-tool page of the
    open-civic-data wiki.

    See: https://github.com/opencivicdata/opencivicdata/wiki/
    '''
    # XXX: This enumeration will eventually come from larvae.
    CLASSIFICATION_CHOICES = mk_choices(['committee', 'party', 'jurisdiction'])

    name = forms.CharField()
    classification = forms.ChoiceField(choices=CLASSIFICATION_CHOICES)
    geography_id = forms.CharField(required=False)

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


class JurisdictionInput(forms.TextInput):

    def _check_value(self, value):
        '''Make sure the passed-in jurisdiction_id isn't
        something like <script>alert("owned")
        '''
    def render(self, name, value, attrs=None):
        return SafeText('<span class="muted">%s/</span>'
                        '<input id="id_jurisdiction_id" '
                        'name="jurisdiction_id" '
                        'type="text" value=""/>' % value)


class CreateForm(EditForm):
    '''A separate form used for creating orgs. Only difference
    is the presence of jurisdiction_id.
    '''
    jurisdiction_id = forms.CharField(widget=JurisdictionInput())

    def _jurisdiction_id_as_popolo(self):
        geo_id = self.data['geography_id']
        jxn_id = self.data['jurisdiction_id']
        return geo_id.replace('-division', '-jurisdiction') + '/' + jxn_id

    def as_popolo(self, request):
        obj = EditForm.as_popolo(self, request)
        obj['jurisdiction_id'] = self._jurisdiction_id_as_popolo()
        return obj


class ListFilterForm(forms.Form):
    CLASSIFICATIONS = mk_choices(
        ['']  + list(db.organizations.distinct('classification')))
    classification = forms.ChoiceField(choices=CLASSIFICATIONS, required=False)
