from django import forms


GEO_CHOICES = [
    ("id1", "name1"),
    ("id2", "name2"),
    ("id3", "name3"),
    ("id4", "name4"),
    ]


class SelectForm(forms.Form):
    '''Provide a form for manual data collection of the fields
    described on the Manual-data-collection-tool page of the
    open-civic-data wiki.

    See: https://github.com/opencivicdata/opencivicdata/wiki/
    '''
    # Required fields.
    geography_id = forms.ChoiceField(choices=GEO_CHOICES)

