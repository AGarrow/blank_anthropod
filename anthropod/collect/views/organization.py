from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.decorators.http import require_POST

import bson.objectid

from ...core import db
from ..forms.organization import EditForm


def create(self):
    return redirect('geo.select')


class Edit(View):

    def get(self, request, geo_id=None, _id=None):
        if _id is not None:
            _id = bson.objectid.ObjectId(_id)
            obj = db.organizations.find_one(_id)
            context = dict(
                obj=obj,
                form=EditForm.from_popolo(obj),
                action='edit')
        else:
            form = EditForm(initial=dict(geography_id=geo_id))
            context = dict(form=form, action='create')
        return render(request, 'organization/edit.html', context)

    def post(self, request, geo_id=None, _id=None):
        form = EditForm(request.POST)
        if form.is_valid():
            popolo_data = form.as_popolo(request)

            # If this request is editing an existing obj,
            # add the id to the popolo data.
            if _id is not None:
                msg = 'Successfully edited organization named %(name)s.'
                _id = bson.objectid.ObjectId(_id)
                popolo_data['_id'] = _id
            else:
                msg = 'Successfully created new organization named %(name)s.'

            _id = db.organizations.save(popolo_data)
            messages.success(request, msg % popolo_data)
            return redirect('organization.detail', _id=_id)
        else:
            return render(request, 'organization/edit.html', dict(form=form))


def detail(request, _id):
    _id = bson.objectid.ObjectId(_id)
    obj = db.organizations.find_one(_id)
    context = dict(obj=obj)
    return render(request, 'organization/detail.html', context)


def listing(request):
    context = {}
    context['organizations'] = list(db.organizations.find())
    return render(request, 'organization/list.html', context)


@require_POST
def delete(request):
    '''Confirm delete.'''
    _id = request.POST.get('_id')
    _id = bson.objectid.ObjectId(_id)
    obj = db.organizations.find_one(_id)
    context = dict(obj=obj)
    return render(request, 'organization/confirm_delete.html', context)


@require_POST
def really_delete(request):
    _id = request.POST.get('_id')
    _id = bson.objectid.ObjectId(_id)
    obj = db.organizations.find_one(_id)
    db.organizations.remove(_id)
    msg = 'Deleted obj %r with id %r.'
    messages.success(request, msg % (obj['name'], _id))
    return redirect(reverse('organization.list'))


# @require_POST
# def remove_person(request, organization_id, person_id):
#     person_id = bson.objectid.ObjectId(person_id)
#     person = db.people.find_one(person_id)
#     del person['organization_id']
#     db.people.save(person)
#     msg = 'Suggessfully removed %s from organization.'
#     messages.success(request, msg % person['name'])
#     kwargs = dict(_id=organization_id)
#     return redirect(reverse('organization.detail', kwargs=kwargs))
