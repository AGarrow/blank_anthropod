from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from ..permissions import check_permissions
from .utils import log_change


class RestrictedView(View):

    check_permissions = staticmethod(check_permissions)
    log_change = staticmethod(log_change)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RestrictedView, self).dispatch(*args, **kwargs)
