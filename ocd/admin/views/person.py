import json

from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.decorators.http import require_POST

import bson.objectid

from ...core import db
from ..models import Person as PersonModel
from ..forms import PersonForm


class Edit(View):

    def get(self, request, _id=None):
        if _id is not None:
            _id = bson.objectid.ObjectId(_id)
            person = db.people.find_one(_id)
            context = dict(
                person=PersonModel(person),
                form=PersonForm.from_popolo(person),
                action='edit')
        else:
            context = dict(form=PersonForm(), action='create')
        return render(request, 'person/create.html', context)

    def post(self, request, _id=None):
        form = PersonForm(request.POST)
        if form.is_valid():
            popolo_data = form.as_popolo(request)

            # If this request is editing an existing person,
            # add the id to the popolo data.
            if _id is not None:
                _id = bson.objectid.ObjectId(_id)
                popolo_data['_id'] = _id

            _id = db.people.save(popolo_data)
            message = 'Successfully, created new person named %(name)s.'
            messages.info(request, message % popolo_data)
            return redirect('person.detail', _id=_id)
        else:
            return render(request, 'person/create.html', dict(form=form))


def detail(request, _id):
    # Get the person data.
    _id = bson.objectid.ObjectId(_id)
    person = db.people.find_one(_id)
    person = PersonModel(person)

    # Stringify the object id.
    person['_id'] = str(person['_id'])

    # Dump the person to json.
    person_json = json.dumps(person, indent=4)
    context = dict(person=person, person_json=person_json)
    return render(request, 'person/detail.html', context)


def listing(request):
    context = {}
    context['people'] = map(PersonModel, db.people.find())
    return render(request, 'person/list.html', context)


@require_POST
def delete(request):
    '''Confirm delete.'''
    _id = request.POST.get('_id')
    _id = bson.objectid.ObjectId(_id)
    person = db.people.find_one(_id)

    # Stringify the object id.
    person['_id'] = str(person['_id'])

    # Dump the person to json.
    person_json = json.dumps(person, indent=4)
    context = dict(
        person=PersonModel(person),
        person_json=person_json)
    return render(request, 'person/confirm_delete.html', context)


def really_delete(request):
    _id = request.POST.get('_id')
    _id = bson.objectid.ObjectId(_id)
    person = db.people.find_one(_id)
    db.people.remove(_id)
    message = 'Deleted person %r with id %r.'
    messages.info(request, message % (person['name'], _id))
    return redirect(reverse('person.list'))
