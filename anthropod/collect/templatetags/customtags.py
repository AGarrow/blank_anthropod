import re
import json
from django import template


register = template.Library()


@register.inclusion_tag('button.html')
def button(obj, viewname, edit_or_delete, method='GET'):
    '''Render an edit or delete button, including all the surrounding
    form guts.
    '''
    icon = {
        'edit': 'icon-edit',
        'delete': 'icon-remove'
        }[edit_or_delete]
    return locals()


class JsonviewFormatter(object):

    def __init__(self, obj):
        self.data = json.dumps(obj, indent=4)

    def ocd_id_replacer(self, matchobj):
        tmpl = '<a href="/collect/{app}/{viewname}/{ocd_id}">{ocd_id}</a>'
        type_ = matchobj.group(1)
        ocd_id = matchobj.group()
        app = {'person': 'person',
                'organization': 'orgs',
                'division': 'geo'}[type_]
        viewname = dict(division='detail').get(type_, 'jsonview')
        return tmpl.format(app=app, ocd_id=ocd_id, viewname=viewname)

    def ocd_ids(self):
        '''Hyperlink any ocd_id's found in the json.
        '''
        rgx = 'ocd-([a-z]+).{,100}'
        self.data = re.sub(rgx, self.ocd_id_replacer, self.data)

    def link_replacer(self, matchobj):
        tmpl = '<a href="{0}">{0}</a>'
        return tmpl.format(matchobj.group(1))

    def links(self):
        rgx = '(http://.+?)"'
        self.data = re.sub(rgx, self.link_replacer, self.data)

    def openstates_id_replacer(self, matchobj):
        leg_id = matchobj.group(1)
        type_ = leg_id[2]
        jurisdiction = leg_id[:2].lower()

        type_ = dict(L='legislators', B='bills', C='committees')[type_]
        tmpl = ('<a href="http://openstates.org/{jurisdiction}/'
                '{type_}/{leg_id}/">{leg_id}</a>')
        repl = tmpl.format(
            leg_id=leg_id, jurisdiction=jurisdiction, type_=type_)
        return matchobj.group().replace(matchobj.group(1), repl)

    def openstates_ids(self):
        rgx = '"([A-Z]{2}[CLB]\d{6})"'
        self.data = re.sub(rgx, self.openstates_id_replacer, self.data)

    def format(self):
        self.ocd_ids()
        self.links()
        self.openstates_ids()
        return self.data


@register.filter
def jsonview(obj):
    return JsonviewFormatter(obj).format()
