import json

from django.views.generic.base import View
from django.shortcuts import render, redirect

import bson.objectid

from ocd.core import db
from ocd.admin import models
from .forms import PersonForm


class CreatePerson(View):

    def get(self, request):
        context = {}
        context['form'] = PersonForm()
        return render(request, 'person/create.html', context)

    def post(self, request):
        form = PersonForm(request.POST)
        if form.is_valid():
            popolo_data = form.as_popolo(request)
            _id = db.people.save(popolo_data)
            return redirect('person', _id=_id)
        else:
            return render(request, 'person/create.html', dict(form=form))


def person(request, _id):
    # Get the person data.
    _id = bson.objectid.ObjectId(_id)
    person = db.people.find_one(_id)
    person = models.Person(person)

    # Stringify the object id.
    person['_id'] = str(person['_id'])

    # Dump the person to json.
    person_json = json.dumps(person, indent=4)
    context = dict(person=person, person_json=person_json)
    return render(request, 'person/detail.html', context)


def person_list(request):
    context = {}
    context['people'] = (models.Person(obj) for obj in db.people.find())
    return render(request, 'person/list.html', context)

