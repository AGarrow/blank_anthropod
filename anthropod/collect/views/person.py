import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied
from django.forms import HiddenInput

import larvae.person
import larvae.membership

from ...core import db, user_db
from ..forms.person import EditForm
from ...models.paginators import CursorPaginator
from ...models.utils import generate_id
from ...models.base import _PrettyPrintEncoder
from ..permissions import check_permissions
from .base import RestrictedView
from .utils import log_change


class Edit(RestrictedView):
    '''Generally, users can edit a person's details if the person is a
    member of an organization the user can edit.

    Users can also create new people as members of organizations they
    can edit.
    '''
    collection = db.people
    validator = larvae.person.Person

    #-------------------------------------------------------------------------
    # Permissions.
    #-------------------------------------------------------------------------
    def check_edit_permissions(self):
        '''Complain unless the user can edit an organization
        that this person is a member of.
        '''
        # Get ids of orgs this user can edit.
        spec = {
            'username': self.request.user.username,
            'permissions': 'organizations.edit',
            }
        org_ids = user_db.permissions.find(spec).distinct('ocd_id')

        # Check it this person_id is a member of any of those orgs.
        spec = {
            'person_id': self.kwargs['_id'],
            'organization_id': {'$in': org_ids}
            }

        # Complain if not.
        if not db.memberships.find_one(spec):
            raise PermissionDenied

    def check_create_member_permissions(self):
        '''Complain unless the user can edit the passed in org_id.
        '''
        org_id = self.request.GET['org_id']
        spec = {
            'username': self.request.user.username,
            'permissions': 'organizations.edit',
            'ocd_id': org_id
            }
        if not user_db.permissions.find_one(spec):
            raise PermissionDenied

    def check_create_permissions(self):
        '''Complain unless the user can create people.
        '''
        spec = {
            'username': self.request.user.username,
            'permissions': 'people.create',
            'ocd_id': None
            }
        if not user_db.permissions.find_one(spec):
            raise PermissionDenied

    #-------------------------------------------------------------------------
    # Get requests return an edit form.
    #-------------------------------------------------------------------------
    def get(self, *args, **kwargs):
        '''Depending on the args supplied, either edit an existing
        person, create a new person as a member of an org, or just
        create a new standalone person.
        '''
        # If a person_id is given, edit an existing person.
        if '_id' in self.request.GET:
            return self.edit_existing()

        # If an org_id is given, create a new person and make
        # the person a member of that org.
        elif 'org_id' in self.request.GET:
            return self.create_member()

        # Else, we're just creating a new person with no association
        # with an org.
        else:
            return self.create()

    def edit_existing(self):
        self.check_edit_permissions()
        _id = self.kwargs['_id']
        person = self.collection.find_one(_id)
        context = dict(
            person=person,
            form=EditForm.from_popolo(person),
            action='edit')
        context['nav_active'] = 'person'
        return render(self.request, 'person/edit.html', context)

    def create_member(self):
        self.check_create_member_permissions()
        org_id = self.request.GET['org_id']
        initial = dict(org_id=org_id)
        context = dict(
            form=EditForm(initial), action='create',
            nav_active='person',
            hidden_input=HiddenInput)
        # f = EditForm(initial)
        # import pdb; pdb.set_trace()
        return render(self.request, 'person/edit.html', context)

    def create(self):
        self.check_create_permissions()
        context = dict(form=EditForm(), action='create', nav_active='person')
        return render(request, 'person/edit.html', context)

    #-------------------------------------------------------------------------
    # Get requests can edit existing or create a new person or member.
    #-------------------------------------------------------------------------
    def post(self, *args, **kwargs):
        form = EditForm(request.POST)
        if form.is_valid():
            obj = form.as_popolo(request)

            if _id is not None:
                # Check permissions.

                # Apply the form changes to the existing object.
                existing_obj = self.collection.find_one(_id)
                existing_obj.update(obj)
                obj = existing_obj
                msg = 'Successfully updated person named %(name)s.'
            else:
                # Check permissions.

                obj['_id'] = generate_id('person')
                msg = 'Successfully created new person named %(name)s.'

            # Check for popolo compliance.
            obj.pop('_type', None)
            obj = self.validator(**obj)
            obj.validate()
            obj = obj.as_dict()

            # Save.
            _id = self.collection.save(obj)
            self.log_change(request, _id, action)
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
def confirm_delete(request):
    _id = request.POST.get('_id')
    person = db.people.find_one(_id)
    check_permissions(request, _id, 'people.delete')
    context = dict(person=person, nav_active='person')
    return render(request, 'person/confirm_delete.html', context)


@require_POST
@login_required
def delete(request):
    _id = request.POST.get('_id')
    action = 'people.delete'
    check_permissions(request, _id, action)
    person = db.people.find_one(_id)
    db.memberships.remove(dict(person_id=person.id))
    db.people.remove(_id)
    log_change(request, _id, action)
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
