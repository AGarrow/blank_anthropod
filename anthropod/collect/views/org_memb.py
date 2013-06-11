from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

import larvae.membership

from ...core import db
from ..permissions import check_permissions
from .base import RestrictedView
from .utils import log_change


def listing(request, _id):
    obj = db.organizations.find_one(_id)
    context = dict(obj=obj, nav_active='org')
    return render(request, 'organization/memb/listing.html', context)


class SelectPerson(RestrictedView):
    '''This page enables the user to choose one or more people to add
    as members to the organization.
    '''
    collection = db.memberships
    validator = larvae.membership.Membership

    def get(self, request, org_id):
        '''Show a form for selecting people to add as members.
        '''
        self.check_permissions(request, org_id, 'organizations.edit')
        context = dict(nav_active='memb', org_id=org_id)
        return render(request, 'organization/memb/select_person.html', context)

    def post(self, request, org_id=None):
        '''Create a membership for each selected person.
        '''

        # Check permissions.
        action = 'memberships.create'
        person_ids = request.POST.getlist('person_id')
        self.check_permissions(request, org_id, action)

        # Create one membership per person_id.
        org_id = request.POST.get('org_id')
        for person_id in person_ids:
            membership = self.validator(
                person_id=person_id,
                organization_id=org_id)
            membership.validate()
            obj = membership.as_dict()
            _id = self.collection.save(obj)
            self.log_change(request, _id, action)

        messages.info(request, 'Created %d new memberships.' % len(person_ids))
        return redirect('org.memb.listing', _id=org_id)


@login_required
def confirm_delete(request):
    _id = request.GET['_id']
    obj = db.memberships.find_one(_id)
    check_permissions(request, obj['organization_id'], 'memberships.delete')
    context = dict(memb=obj, nav_active='org')
    return render(request, 'organization/memb/confirm_delete.html', context)


@require_POST
@login_required
def delete(request):
    '''This is the view that handles deletions from clicking on the
    inline buttons in the org.memb.listing view. It (arguably) needs its
    own view to redirect back to the org's membership list.
    '''
    # Retrieve the membership object.
    _id = request.POST['_id']
    obj = db.memberships.find_one(_id)

    # Make sure user can delete.
    action = 'memberships.delete'
    check_permissions(request, obj['organization_id'], action)

    # Delete and log the change.
    db.memberships.remove(_id)
    log_change(request, _id, action)

    # Generate a flash message.
    vals = (obj.person().display(), obj.organization().display())
    msg = "Deleted %s's membership in %r." % vals
    messages.info(request, msg)

    kwargs = dict(_id=obj.organization().id)
    return redirect(reverse('org.memb.listing', kwargs=kwargs))
