from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class RestrictedView(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RestrictedView, self).dispatch(*args, **kwargs)
