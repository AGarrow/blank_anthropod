from django.views.generic.base import View
from django.shortcuts import render, redirect

import bson.objectid

from ocd.core import db
from .forms import PersonForm


class CreatePerson(View):

    def get(self, request):
        context = {}
        context['form'] = PersonForm()
        return render(request, 'person/create.html', context)

    def post(self, request):
        form = PersonForm(request.POST)
        popolo_data = form.as_popolo()
        _id = db.people.save(popolo_data)
        return redirect('person', _id=_id)


def person(request, _id):
    _id = bson.objectid.ObjectId(_id)
    person = db.people.find_one(_id)
    context = dict(person=person)
    return render(request, 'person/detail.html', context)


