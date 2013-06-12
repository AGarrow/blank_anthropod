from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

import larvae.membership

from ...core import db
from ..forms.memb import EditForm
from ..permissions import check_permissions
from .base import RestrictedView
from .utils import log_change


class Edit(RestrictedView):

    collection = db.memberships
    validator = larvae.membership.Membership
    form_class = EditForm

    def get(self, request):
        _id = self.form.data.get('_id')
        if _id is not None:
            # Edit an existing object.
            obj = self.collection.find_one(_id)

            self.check_permissions(
                request, obj['organization_id'], 'organizations.edit')

            context = dict(
                obj=obj,
                form=EditForm.from_popolo(obj),
                action='edit')
        else:
            self.check_permissions(request, _id, 'memberships.create')

            # Create a new object.
            context = dict(form=EditForm(), action='create')
        context['nav_active'] = 'memb'
        return render(request, 'memb/edit.html', context)

    def post(self, request, _id=None):
        if self.form.is_valid():
            obj = self.form.as_popolo(request)
            _id = self.form.data.get('_id')
            org_id = self.form.data['organization_id']
            unset_fields = set()
            if _id is not None:
                check_permissions(request, org_id, 'organizations.edit')
                action = 'memberships.edit'
                existing_obj = self.collection.find_one(_id)

                # Determine whether any fields have been unset.
                unset_fields = set(existing_obj) - set(obj)
                for field in set(unset_fields):
                    if field.startswith('_'):
                        unset_fields.remove(field)

                # Apply the form changes to the existing object.
                existing_obj.update(obj)
                obj = existing_obj
                msg = "Successfully edited %s's membership in %s."
            else:
                action = 'memberships.create'
                check_permissions(request, _id, 'organizations.edit')
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

            # And unset the emtpy fields, i.e., where someone field contents.
            if unset_fields:
                doc = {'$unset': dict.fromkeys(unset_fields)}
                self.collection.update(obj, doc)

            messages.success(request, msg % msg_args)
            return redirect('memb.jsonview', _id=_id)
        else:
            obj = self.collection.find_one(_id)
            return render(request, 'memb/edit.html', dict(form=form, obj=obj))


def jsonview(request, _id):
    obj = db.memberships.find_one(_id)
    context = dict(obj=obj, nav_active='memb')
    return render(request, 'memb/jsonview.html', context)


@login_required
def confirm_delete(request):
    '''Confirm delete.'''
    # Get the membership id.
    _id = request.GET['_id']
    obj = db.memberships.find_one(_id)
    check_permissions(request, obj['organization_id'], 'memberships.delete')

    context = dict(memb=obj, nav_active='person')
    return render(request, 'memb/confirm_delete.html', context)


@require_POST
@login_required
def delete(request):
    '''This is the view that handles deletions from a membership
    detail page. Deletions from clicking inline on the buttons on
    person.memb.listing and org.memb.listing views are handled by
    person.memb.confirm_delete and organization.memb.confirm_delete,
    respectively. Each of those redirects to the person or org
    membership listing.
    '''
    # Get the object.
    _id = request.POST['_id']
    obj = db.memberships.find_one(_id)

    # Check permissions.
    check_permissions(request, obj['organization_id'], 'memberships.delete')

    # Format a flash message.
    vals = (obj.person().display(), obj.organization().display())
    msg = "Deleted %s's membership in %s."
    messages.info(request, msg % vals)

    # Remove the object.
    db.memberships.remove(_id)
    log_change(request, _id, 'memberships.delete')

    kwargs = dict(_id=obj.person().id)
    return redirect(reverse('org.memb.listing', kwargs=kwargs))
