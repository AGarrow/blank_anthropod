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
