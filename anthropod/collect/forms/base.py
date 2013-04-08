from django import forms


def mk_choices(iterable):
    return zip(iterable, iterable)


class BaseForm(forms.Form):

    def __iter__(self):
        '''When displaying the form with {% for field in form %},
        only display fields that don't begin with "alternate_name",
        "contact", or "link".
        '''
        skip = ('contact', 'link', 'alternate_name')
        for field in super(BaseForm, self).__iter__():
            if not field.name.startswith(skip):
                yield field

    @classmethod
    def single_fields(cls):
        for name, field in cls.base_fields.items():
            if not name.startswith(('contact', 'alternate_name', 'link')):
                yield name, field

    # Methods for converting form data into popolo data.
    def _get_zipped_field_data(self, request, prefix, fields, asdict=True):
        '''POST.getlist the values of fields prefixed with `prefix`
        and zip them together. Generate a sequence of dicts.
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


class HasContactInfo(BaseForm):
    '''A mixin class for adding contact info to a form.
    '''
    CONTACT_TYPE_CHOICES = mk_choices([
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

    def contact(self, request):
        '''Return this form's contact data as a list of
        (type, value, note) 3-tuples like ('voice', '12344567', 'home').
        '''
        return self.zipfields(request,
                              prefix='contact_',
                              fields=('type', 'value', 'note'),
                              asdict=False)
