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
    context = dict(
        person=db.people.find_one(_id),
        nav_active='person')
    return render(request, 'person/memb/listing.html', context)


# Views for adding/deleting memberships.
class SelectGeo(RestrictedView):
    '''This page enables the user to choose a geography within
    which to search for organizations to create a membership
    for this person.
    '''
    def get(self, request):
        context = dict(
            person_id=request.GET['person_id'],
            nav_active='person')
        return render(request, 'person/memb/select_geo.html', context)

    def post(self, request, person_id):
        _id = request.POST.get('id')
        url_kwargs = dict(geo_id=_id, person_id=person_id)
        return redirect('person.memb.add.org', **url_kwargs)


class SelectOrg(RestrictedView):
    '''This page enables the user to choose an organization within
    a georgraphy to create a membership for this person.
    '''
    collection = db.memberships
    validator = larvae.membership.Membership

    def get(self, request):
        '''The geo_id is named `id` because we're reusing the geo select
        template for the referer page.
        '''
        person_id = request.GET['person_id']
        geo_id = request.GET['id']
        context = dict(
            nav_active='person',
            person_id=person_id,
            geo_id=geo_id)
        return render(request, 'person/memb/select_org.html', context)

    def post(self, request):
        org_ids = request.POST.getlist('org_id')
        person_id = request.POST['person_id']
        for org_id in org_ids:
            self.check_permissions(request, org_id, 'memberships.create')
            membership = self.validator(
                person_id=person_id,
                organization_id=org_id)
            membership.validate()
            obj = membership.as_dict()
            membership_id = self.collection.save(obj)
            self.log_change(request, membership_id, 'membership.create')
        messages.info(request, 'Created %d new memberships.' % len(org_ids))
        return redirect('person.memb.listing', _id=person_id)


@login_required
def confirm_delete(request):
    '''Confirm delete.'''
    # Get the membership id.
    _id = request.GET['_id']
    obj = db.memberships.find_one(_id)
    check_permissions(request, obj['organization_id'], 'memberships.delete')
    context = dict(memb=obj, nav_active='person')
    return render(request, 'person/memb/confirm_delete.html', context)


@require_POST
@login_required
def delete(request):
    '''This is the view that handles deletions from clicking on the
    inline buttons in the person.memb.listing view. It (arguably) needs its
    own view in order to redirect back to the person's membership list.
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

    # Redirect to the person's membership listing.
    return redirect(reverse('person.jsonview', kwargs=kwargs))
