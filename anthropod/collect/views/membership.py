from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST

import larvae.membership

from ...core import db
from ...models.utils import get_id
from ..forms.memb import EditForm


class Edit(View):

    collection = db.memberships
    validator = larvae.membership.Membership

    def get(self, request, _id=None):
        if _id is not None:
            # Edit an existing object.
            _id = get_id(_id)
            obj = self.collection.find_one(_id)
            context = dict(
                obj=obj,
                form=EditForm.from_popolo(obj),
                action='edit')
        else:
            # Create a new object.
            context = dict(form=EditForm(), action='create')
        context['nav_active'] = 'memb'
        return render(request, 'memb/edit.html', context)

    def post(self, request, _id=None):
        form = EditForm(request.POST)
        if form.is_valid():
            obj = form.as_popolo(request)

            if _id is not None:
                # Apply the form changes to the existing object.
                _id = get_id(_id)
                existing_obj = self.collection.find_one(_id)
                existing_obj.update(obj)
                obj = existing_obj
                msg = "Successfully edited %s's membership in %s."
            else:
                msg = "Successfully edited %s's membership in %s."
            msg_args = (obj.person().display(), obj.organization().display())

            # Validate the org.
            obj = self.validator(**obj)
            obj.validate()
            obj = obj.as_dict()

            # Save.
            _id = self.collection.save(obj)
            messages.success(request, msg % msg_args)
            return redirect('memb.jsonview', _id=_id)
        else:
            return render(request, 'memb/edit.html', dict(form=form))


def jsonview(request, _id):
    _id = get_id(_id)
    obj = db.memberships.find_one(_id)
    context = dict(obj=obj, nav_active='memb')
    return render(request, 'memb/jsonview.html', context)


@require_POST
def delete(request, _id):
    pass