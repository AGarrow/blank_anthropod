import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

import larvae.person
import larvae.membership

from ...core import db
from ..forms.person import EditForm
from ...models.paginators import CursorPaginator
from ...models.utils import get_id, generate_id
from ...models.base import _PrettyPrintEncoder
from .base import RestrictedView


class Edit(RestrictedView):

    collection = db.people
    validator = larvae.person.Person

    def get(self, request, _id=None):
        if _id is not None:
            # Edit an existing object.
            _id = get_id(_id)
            person = self.collection.find_one(_id)
            context = dict(
                person=person,
                form=EditForm.from_popolo(person),
                action='edit')
        else:
            # Create a new object.
            context = dict(form=EditForm(), action='create')
        context['nav_active'] = 'person'
        return render(request, 'person/edit.html', context)

    def post(self, request, _id=None):
        form = EditForm(request.POST)
        if form.is_valid():
            obj = form.as_popolo(request)

            if _id is not None:
                # Apply the form changes to the existing object.
                existing_obj = self.collection.find_one(_id)
                existing_obj.update(obj)
                obj = existing_obj
                msg = 'Successfully updated person named %(name)s.'
            else:
                obj['_id'] = generate_id('person')
                msg = 'Successfully created new person named %(name)s.'

            # Check for popolo compliance.
            obj.pop('_type', None)
            obj = self.validator(**obj)
            obj.validate()
            obj = obj.as_dict()

            # Save.
            _id = self.collection.save(obj)
            messages.info(request, msg % obj)
            return redirect('person.jsonview', _id=_id)
        else:
            obj = self.collection.find_one(_id)
            context = dict(form=form, obj=obj)
            return render(request, 'person/edit.html', context)



def listing(request):
    context = dict(nav_active='person')
    page = int(request.GET.get('page', 1))
    people = db.people.find()
    context['people'] = CursorPaginator(people, page=page, show_per_page=10)
    return render(request, 'person/listing.html', context)


@require_POST
@login_required
def delete(request):
    '''Confirm delete.'''
    _id = request.POST.get('_id')
    person = db.people.find_one(_id)
    context = dict(person=person, nav_active='person')
    return render(request, 'person/confirm_delete.html', context)


@require_POST
@login_required
def really_delete(request):
    _id = request.POST.get('_id')
    _id = get_id(_id)
    person = db.people.find_one(_id)
    db.memberships.remove(dict(person_id=person.id))
    db.people.remove(_id)
    msg = 'Deleted person %r with id %r.'
    messages.info(request, msg % (person['name'], _id))
    return redirect('person.listing')


def all_json(request):
    '''Return typeahead widget people json.
    '''
    data = []
    fields = ('name',)
    for obj in db.people.find({}, fields):
        obj['value'] = obj.display()
        del obj['name']
        data.append(obj)
    resp = HttpResponse(mimetype='application/json', status=200)
    json.dump(data, resp, cls=_PrettyPrintEncoder)
    return resp


def jsonview(request, _id):
    # Get the person data.
    context = dict(
        person=db.people.find_one(_id),
        nav_active='person')
    return render(request, 'person/jsonview.html', context)
