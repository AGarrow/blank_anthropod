from django.core.exceptions import PermissionDenied

from anthropod.core import user_db


def check_permissions(request, *permissions):
    '''Check whether the request.user has the specified permissions;
    if not, raise PermissionDenied.
    '''
    spec = {
        'user_id': request.user.username,
        '$or': [

            # Allow all permissions for admins.
            {'*': True},

            # Or explicitly set permissions.
            dict.fromkeys(permissions, True),
            ],
        }

    if not user_db.permissions.find_one(spec):

        # Hack for passing context data to PermissionDenied. May be
        # supported in django soon.
        # See https://code.djangoproject.com/ticket/20156.
        request.anthropod_permissions = permissions

        raise PermissionDenied()
