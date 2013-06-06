from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

import larvae.membership

from ...core import db
from ..forms.memb import EditForm
from ..permissions import check_permissions, any_permissions
from .base import RestrictedView
from .utils import log_change


class Edit(RestrictedView):

    collection = db.memberships
    validator = larvae.membership.Membership

    def get(self, request, _id=None):
        if _id is not None:
            # Edit an existing object.
            obj = self.collection.find_one(_id)

            self.any_permissions(request, [
                (obj['organization_id'], ['organizations.edit']),
                (obj['person_id'], ['people.edit'])])

            context = dict(
                obj=obj,
                form=EditForm.from_popolo(obj),
                action='edit')
        else:
            check_permissions(request, _id, 'memberships.create')

            # Create a new object.
            context = dict(form=EditForm(), action='create')
        context['nav_active'] = 'memb'
        return render(request, 'memb/edit.html', context)

    def post(self, request, _id=None):
        form = EditForm(request.POST)
        if form.is_valid():
            obj = form.as_popolo(request)

            if _id is not None:
                action = 'memberships.edit'
                check_permissions(request, _id, action)

                # Apply the form changes to the existing object.
                existing_obj = self.collection.find_one(_id)
                existing_obj.update(obj)
                obj = existing_obj
                msg = "Successfully edited %s's membership in %s."
            else:
                action = 'memberships.create'
                check_permissions(request, _id, action)

                msg = "Successfully created %s's membership in %s."

            msg_args = (obj.person().display(), obj.organization().display())

            # Validate the org.
            obj.pop('_type', None)
            obj = self.validator(**obj)
            obj.validate()
            obj = obj.as_dict()

            # Save.
            _id = self.collection.save(obj)
            self.log_change(request, _id, action)
            messages.success(request, msg % msg_args)
            return redirect('memb.jsonview', _id=_id)
        else:
            obj = self.collection.find_one(_id)
            return render(request, 'memb/edit.html', dict(form=form, obj=obj))


def jsonview(request, _id):
    obj = db.memberships.find_one(_id)
    context = dict(obj=obj, nav_active='memb')
    return render(request, 'memb/jsonview.html', context)


@require_POST
@login_required
def confirm_delete(request):
    '''Confirm delete.'''
    # Get the membership id.
    _id = request.POST.get('_id')
    obj = db.memberships.find_one(_id)

    any_permissions(request, [
        (obj['organization_id'], ['organizations.edit']),
        (obj['person_id'], ['people.edit'])])

    context = dict(memb=obj, nav_active='person')
    return render(request, '/memb/confirm_delete.html', context)


@require_POST
@login_required
def delete(request):
    # Get the object.
    _id = request.POST.get('_id')
    obj = db.memberships.find_one(_id)

    # Check permissions.
    any_permissions(request, [
        (obj['organization_id'], ['organizations.edit']),
        (obj['person_id'], ['people.edit'])])

    # Format a flash message.
    vals = (obj.person().display(), obj.organization().display())
    msg = "Deleted %s's membership in %s."
    messages.info(request, msg % vals)

    # Remove the object.
    db.memberships.remove(_id)
    log_change(request, _id, 'memberships.delete')

    kwargs = dict(_id=obj.person().id)
    return redirect(reverse('person.memb.listing', kwargs=kwargs))
