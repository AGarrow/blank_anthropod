from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

import larvae.membership

from ...core import db
from ...models.utils import get_id
from .base import RestrictedView


def listing(request, _id):
    _id = get_id(_id)
    obj = db.organizations.find_one(_id)
    context = dict(obj=obj, nav_active='org')
    return render(request, 'organization/memb/listing.html', context)


class SelectPerson(RestrictedView):
    '''This page enables the user to choose an organization within
    a georgraphy to create a membership for this person.
    '''
    collection = db.memberships
    validator = larvae.membership.Membership

    def get(self, request, org_id):
        context = dict(nav_active='memb', org_id=org_id)
        return render(request, 'organization/memb/select_person.html', context)

    def post(self, request, org_id=None):
        person_ids = request.POST.getlist('person_id')
        org_id = request.POST.get('org_id')
        for person_id in person_ids:
            membership = self.validator(
                person_id=person_id,
                organization_id=org_id)
            membership.validate()
            obj = membership.as_dict()
            self.collection.save(obj)
        messages.info(request, 'Created %d new memberships.' % len(person_ids))
        return redirect('org.memb.listing', _id=org_id)


@require_POST
@login_required
def delete(request):
    '''Confirm delete.'''
    # Get the membership id.
    _id = request.POST.get('_id')
    _id = get_id(_id)
    memb = db.memberships.find_one(_id)
    context = dict(memb=memb, nav_active='org')
    return render(request, 'organization/memb/confirm_delete.html', context)


@require_POST
@login_required
def really_delete(request):
    # Get the membership id.
    _id = request.POST.get('_id')
    _id = get_id(_id)

    obj = db.memberships.find_one(_id)
    vals = (obj.person().display(), obj.organization().display())
    msg = "Deleted %s's membership in %r." % vals
    kwargs = dict(_id=obj.organization().id)
    db.memberships.remove(_id)
    messages.info(request, msg)
    return redirect(reverse('organization.jsonview', kwargs=kwargs))
