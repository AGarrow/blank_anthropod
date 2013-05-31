from .core import check_permissions


class PermissionsMiddleware(object):
    '''Middleware that checks if a view is marked as requiring permissions
    (by .decorators.permissions_required), and if so, checks the permissions,
    which raises django.core.exceptions.PermissionDenied if none are found.
    '''
    def process_view(self, request, view, view_args, view_kwargs):
        permissions = getattr(view, '_anthropod_permissions', None)
        if permissions is None:
            return
        check_permissions(request, *permissions)
