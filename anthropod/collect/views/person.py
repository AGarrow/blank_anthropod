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
from ...utils import Cached
from ..forms.person import EditForm
from ...models.paginators import CursorPaginator
from ...models.utils import generate_id
from ...models.base import _PrettyPrintEncoder
from ..permissions import PermissionChecker, check_permissions, check_admin
from .base import RestrictedView
from .utils import log_change


class PermissionChecker(PermissionChecker):

    form_class = EditForm

    def check_edit(self):
        '''Complain unless the user can edit an organization
        that this person is a member of.
        '''
        if self.check_admin(self.request):
            return
        # Get ids of orgs this user can edit.
        spec = {
            'username': self.request.user.username,
            'permissions': 'organizations.edit',
            }
        org_ids = user_db.permissions.find(spec).distinct('ocd_id')

        # Check if this person_id is a member of any of those orgs.
        spec = {
            'person_id': self.form.data['_id'],
            'organization_id': {'$in': org_ids}
            }

        # Complain if not.
        if not db.memberships.find_one(spec):
            raise self.PermissionDenied

    def check_create_member(self):
        '''Complain unless the user can edit the passed in org_id.
        '''
        if self.check_admin(self.request):
            return
        org_id = self.form.data['org_id']
        spec = {
            'username': self.request.user.username,
            'permissions': 'organizations.edit',
            'ocd_id': org_id
            }
        if not user_db.permissions.find_one(spec):
            raise PermissionDenied

    def check_create(self):
        '''Complain unless the user can create people.
        '''
        if self.check_admin(self.request):
            return
        spec = {
            'username': self.request.user.username,
            'permissions': 'people.create',
            'ocd_id': None
            }
        if not user_db.permissions.find_one(spec):
            raise PermissionDenied


class Edit(RestrictedView):
    '''Generally, users can edit a person's details if the person is a
    member of an organization the user can edit.

    Users can also create new people as members of organizations they
    can edit.
    '''
    collection = db.people
    validator = larvae.person.Person
    form_class = EditForm
    permission_checker_class = PermissionChecker

    #-------------------------------------------------------------------------
    # GET requests will return an edit form.
    #-------------------------------------------------------------------------
    def get(self, *args, **kwargs):
        '''Depending on the args supplied, either edit an existing
        person, create a new person as a member of an org, or just
        create a new standalone person.
        '''
        # If a person_id is given, edit an existing person.
        if '_id' in self.request.GET:
            return self.get_edit_existing()

        # If an org_id is given, create a new person and make
        # the person a member of that org.
        elif 'org_id' in self.request.GET:
            return self.get_create_member()

        # Else, we're just creating a new person with no association
        # with an org.
        else:
            return self.get_create()

    def get_edit_existing(self):
        self.permission_checker.check_edit()
        _id = self.form.data['_id']
        person = self.collection.find_one(_id)
        context = dict(
            person=person,
            form=EditForm.from_popolo(person),
            action='edit')
        context['nav_active'] = 'person'
        return render(self.request, 'person/edit.html', context)

    def get_create_member(self):
        self.permission_checker.check_create_member()
        org_id = self.request.GET['org_id']
        initial = dict(org_id=org_id)
        context = dict(
            form=EditForm(initial), action='create',
            nav_active='person',
            hidden_input=HiddenInput)
        # f = EditForm(initial)
        # import pdb; pdb.set_trace()
        return render(self.request, 'person/edit.html', context)

    def get_create(self):
        self.permission_checker.check_create()
        context = dict(form=EditForm(), action='create', nav_active='person')
        return render(self.request, 'person/edit.html', context)

    #-------------------------------------------------------------------------
    # POST requests can edit existing or create a new person or member.
    #-------------------------------------------------------------------------
    def post(self, *args, **kwargs):
        if self.form.is_valid():
            # If a person_id is given, edit an existing person.
            if '_id' in self.request.GET:
                return self.post_edit_existing()

            # If an org_id is given, create a new person and make
            # the person a member of that org.
            elif 'org_id' in self.request.GET:
                return self.post_create_member()

            # Else, we're just creating a new person with no association
            # with an org.
            else:
                return self.post_create()
        else:
            _id = self.form.data['_id']
            obj = self.collection.find_one(_id)
            context = dict(form=self.form, obj=obj)
            return render(self.request, 'person/edit.html', context)

    def obj_as_popolo(self, obj):
        '''Check for popolo compliance.
        '''
        obj.pop('_type', None)
        obj = self.validator(**obj)
        obj.validate()
        return obj.as_dict()

    def post_edit_existing(self):
        self.permission_checker.check_edit()
        obj = self.form.as_popolo(self.request)
        _id = self.form.data['_id']

        # Apply the form changes to the existing object.
        existing_obj = self.collection.find_one(_id)
        existing_obj.update(obj)
        obj = existing_obj
        msg = 'Successfully updated person named %(name)s.'

        # Validate and save.
        obj = self.obj_as_popolo(obj)
        _id = self.collection.save(obj)

        messages.info(self.request, msg % obj)
        self.log_change(self.request, _id, 'person.edit')
        return redirect('person.jsonview', _id=_id)

    def post_create_member(self):
        '''Create a new person as a member of this organization.
        '''
        self.permission_checker.check_create_member()

        obj = self.form.as_popolo(self.request)
        obj['_id'] = generate_id('person')
        msg = 'Successfully created new member named %(name)s.'

        # Validate and save.
        org_id = obj.pop('org_id')
        self.obj_as_popolo(obj)
        person_id = self.collection.save(obj)

        self.log_change(self.request, person_id, 'person.create')
        messages.info(self.request, msg % obj)

        # Add the membership.
        obj = dict(
            person_id=person_id,
            organization_id=org_id)

        obj = larvae.membership.Membership(**obj)
        obj.validate()
        obj = obj.as_dict()

        # Save.
        _id = db.memberships.save(obj)
        self.log_change(self.request, _id, 'membership.create')
        return redirect('org.memb.listing', _id=org_id)

    def post_create(self):
        self.permission_checker.check_create()

        obj = self.form.as_popolo(self.request)
        obj['_id'] = generate_id('person')
        msg = 'Successfully created new person named %(name)s.'

        # Validate and save.
        obj = self.obj_as_popolo(obj)
        _id = self.collection.save(obj)
        self.log_change(self.request, _id, 'person.create')
        messages.info(self.request, msg % obj)
        return redirect('person.jsonview', _id=_id)


def listing(request):
    context = dict(nav_active='person')
    page = int(request.GET.get('page', 1))
    people = db.people.find()
    context['people'] = CursorPaginator(people, page=page, show_per_page=10)
    return render(request, 'person/listing.html', context)


@login_required
def confirm_delete(request):
    _id = request.GET['_id']
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
