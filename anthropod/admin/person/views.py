from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.decorators.http import require_POST

import bson.objectid

from ...core import db

from .forms import getform


class Edit(View):

    def get(self, request, _id=None):
        if _id is not None:
            _id = bson.objectid.ObjectId(_id)
            person = db.people.find_one(_id)
            context = dict(
                person=person,
                form=getform().from_popolo(person),
                action='edit')
        else:
            context = dict(form=getform(), action='create')
        return render(request, 'person/edit.html', context)

    def post(self, request, _id=None):
        form = getform()(request.POST)
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
            return render(request, 'person/edit.html', dict(form=form))


def detail(request, _id):
    # Get the person data.
    _id = bson.objectid.ObjectId(_id)
    person = db.people.find_one(_id)
    context = dict(person=person)
    return render(request, 'person/detail.html', context)


def listing(request):
    context = {}
    context['people'] = db.people.find()
    return render(request, 'person/list.html', context)


@require_POST
def delete(request):
    '''Confirm delete.'''
    _id = request.POST.get('_id')
    _id = bson.objectid.ObjectId(_id)
    person = db.people.find_one(_id)
    context = dict(person=person)
    return render(request, 'person/confirm_delete.html', context)


@require_POST
def really_delete(request):
    _id = request.POST.get('_id')
    _id = bson.objectid.ObjectId(_id)
    person = db.people.find_one(_id)
    db.people.remove(_id)
    message = 'Deleted person %r with id %r.'
    messages.info(request, message % (person['name'], _id))
    return redirect(reverse('person.list'))
