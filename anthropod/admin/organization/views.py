import json

from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.decorators.http import require_POST

import bson.objectid

from ...core import db
from ...models import Organization as Model
from .forms import EditForm


class Edit(View):

    def get(self, request, _id=None):
        if _id is not None:
            _id = bson.objectid.ObjectId(_id)
            obj = db.organizations.find_one(_id)
            context = dict(
                obj=Model(obj),
                form=EditForm.from_popolo(obj),
                action='edit')
        else:
            context = dict(form=EditForm(), action='create')
        return render(request, 'organization/create.html', context)

    def post(self, request, _id=None):
        form = EditForm(request.POST)
        if form.is_valid():
            popolo_data = form.as_popolo(request)

            # If this request is editing an existing obj,
            # add the id to the popolo data.
            if _id is not None:
                _id = bson.objectid.ObjectId(_id)
                popolo_data['_id'] = _id

            _id = db.organizations.save(popolo_data)
            message = 'Successfully, created new organization named %(name)s.'
            messages.info(request, message % popolo_data)
            return redirect('obj.detail', _id=_id)
        else:
            return render(request, 'organization/create.html', dict(form=form))


def detail(request, _id):
    # Get the obj data.
    _id = bson.objectid.ObjectId(_id)
    obj = db.organizations.find_one(_id)
    obj = Model(obj)

    # Stringify the object id.
    obj['_id'] = str(obj['_id'])

    # Dump the obj to json.
    obj_json = json.dumps(obj, indent=4)
    context = dict(obj=obj, obj_json=obj_json)
    return render(request, 'organization/detail.html', context)


def listing(request):
    context = {}
    context['organizations'] = map(Model, db.organizations.find())
    return render(request, 'organization/list.html', context)


@require_POST
def delete(request):
    '''Confirm delete.'''
    _id = request.POST.get('_id')
    _id = bson.objectid.ObjectId(_id)
    obj = db.organizations.find_one(_id)

    # Stringify the object id.
    obj['_id'] = str(obj['_id'])

    # Dump the obj to json.
    obj_json = json.dumps(obj, indent=4)
    context = dict(
        obj=Model(obj),
        obj_json=obj_json)
    return render(request, 'organization/confirm_delete.html', context)


@require_POST
def really_delete(request):
    _id = request.POST.get('_id')
    _id = bson.objectid.ObjectId(_id)
    obj = db.organizations.find_one(_id)
    db.organizations.remove(_id)
    message = 'Deleted obj %r with id %r.'
    messages.info(request, message % (obj['name'], _id))
    return redirect(reverse('organization.list'))
