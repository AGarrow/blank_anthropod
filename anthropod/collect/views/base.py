from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from ...utils import Cached
from ..permissions import (check_permissions, check_admin,
                           PermissionChecker)
from .utils import log_change


class RestrictedView(View):

    check_admin = check_admin
    check_permissions = staticmethod(check_permissions)
    log_change = staticmethod(log_change)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RestrictedView, self).dispatch(*args, **kwargs)

    #-------------------------------------------------------------------------
    # Helpers
    #-------------------------------------------------------------------------
    @Cached
    def form(self):
        '''Return the request form. Requires a view-level attribute
        of `form_class` to be set.
        '''
        formdata = getattr(self.request, self.request.method)
        return self.form_class(formdata)

    @property
    def permission_checker(self):
        return self.permission_checker_class(self.request)
