import json

from django.http import HttpResponse
from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

import larvae.organization

from ...core import db
from ...models.paginators import CursorPaginator
from ...models.base import _PrettyPrintEncoder
from ...models.utils import get_id, generate_id
from ..forms.organization import EditForm
from .base import RestrictedView


def create(self):
    return redirect('geo.select')


class Edit(RestrictedView):

    collection = db.organizations
    validator = larvae.organization.Organization

    def get(self, request, geo_id=None, _id=None):
        if _id is not None:
            # Edit an existing object.
            _id = get_id(_id)
            obj = self.collection.find_one(_id)
            context = dict(
                obj=obj,
                form=EditForm.from_popolo(obj),
                action='edit')
        else:
            # Create a new object.
            form = EditForm(initial=dict(geography_id=geo_id))
            context = dict(form=form, action='create')
        context['nav_active'] = 'org'
        return render(request, 'organization/edit.html', context)

    def post(self, request, geo_id=None, _id=None):
        form = EditForm(request.POST)
        if form.is_valid():
            obj = form.as_popolo(request)

            if _id is not None:
                # Apply the form changes to the existing object.
                _id = get_id(_id)
                existing_obj = self.collection.find_one(_id)
                existing_obj.update(obj)
                obj = existing_obj
                msg = 'Successfully edited organization named %(name)s.'
            else:
                obj['_id'] = generate_id('organization')
                msg = 'Successfully created new organization named %(name)s.'

            # Validate the org.
            obj.pop('_type', None)
            obj = self.validator(**obj)
            obj.validate()
            obj = obj.as_dict()

            # Save.
            _id = self.collection.save(obj)
            messages.success(request, msg % obj)
            return redirect('organization.jsonview', _id=_id)
        else:
            obj = self.collection.find_one(_id)
            context = dict(form=form, obj=obj)
            return render(request, 'organization/edit.html', context)


def jsonview(request, _id):
    _id = get_id(_id)
    obj = db.organizations.find_one(_id)
    context = dict(obj=obj, nav_active='org')
    return render(request, 'organization/jsonview.html', context)


def listing(request):
    context = dict(nav_active='org')
    page = int(request.GET.get('page', 1))
    orgs = db.organizations.find()
    context['organizations'] = CursorPaginator(orgs, page=page, show_per_page=10)
    return render(request, 'organization/list.html', context)


@require_POST
@login_required
def delete(request):
    '''Confirm delete.'''
    _id = request.POST.get('_id')
    _id = get_id(_id)
    obj = db.organizations.find_one(_id)
    context = dict(obj=obj, nav_active='org')
    return render(request, 'organization/confirm_delete.html', context)


@require_POST
@login_required
def really_delete(request):
    _id = request.POST.get('_id')
    _id = get_id(_id)
    obj = db.organizations.find_one(_id)
    db.memberships.remove(dict(organization_id=obj.id))
    db.organizations.remove(_id)
    msg = 'Deleted obj %r with id %r.'
    messages.success(request, msg % (obj['name'], _id))
    return redirect(reverse('organization.list'))


def json_for_geo(request, geo_id):
    '''Return typeahead widget orgs json for a given geo_id.
    '''
    data = []
    spec = dict(geography_id=geo_id)
    fields = ('name',)
    for org in db.organizations.find(spec, fields):
        org['value'] = org.display()
        del org['name']
        data.append(org)

    resp = HttpResponse(mimetype='application/json', status=200)
    json.dump(data, resp, cls=_PrettyPrintEncoder)
    return resp
