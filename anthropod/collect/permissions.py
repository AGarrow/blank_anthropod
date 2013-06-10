import logging

from django.core.exceptions import PermissionDenied
from django.conf import settings

from anthropod.core import user_db
from anthropod.utils import Cached


logger = logging.getLogger(__name__)


def check_admin(request):
    username = request.user.username
    profile = user_db.profiles.find_one(username) or {}
    if profile.get('is_admin'):
        return True


def check_permissions(request, ocd_id, *permissions):
    '''Check whether the request.user has the specified permissions;
    if not, raise PermissionDenied.
    '''
    if check_admin(request):
        return True

    spec = {
        'username': request.user.username,
        'permissions': {'$all': permissions},
        }

    if ocd_id is not None:
        spec.update(ocd_id=ocd_id)

    if not user_db.permissions.find_one(spec):

        # Hack for passing context data to PermissionDenied. May be
        # supported in django soon.
        # See https://code.djangoproject.com/ticket/20156.
        request.anthropod_ocd_id = ocd_id
        request.anthropod_permissions = permissions

        raise PermissionDenied()


def grant_permissions(username, ocd_id, *permissions):
    spec = {
        'username': username,
        'ocd_id': ocd_id,
        }
    document = {
        '$addToSet': {'permissions': {'$each': permissions}}
        }
    user_db.permissions.update(spec, document, upsert=True, multi=True)
    args = (username, permissions)
    logger.info('Granted the following permissions to %r: %r' % args)


def revoke_permissions(username, ocd_id, *permissions):
    spec = dict(username=username)
    if ocd_id is not None:
        spec.update(ocd_id=ocd_id)
    document = {
        '$pullAll': {'permissions': permissions}
        }
    user_db.permissions.update(spec, document, upsert=True, multi=True)
    args = (username, permissions)
    logger.info('Revoked the following permissions from %r: %r' % args)


class PermissionChecker(object):
    '''This class provides shortcuts for the boilerplate permissions
    checking code. The permissions-checking functions are all available
    on the class.
    '''

    # Make these accessible on the class.
    check_permissions = staticmethod(check_permissions)
    check_admin = staticmethod(check_admin)
    PermissionDenied = staticmethod(PermissionDenied)

    # Subclasses set this--used in the `form` method below.
    form_class = None

    def __init__(self, request):
        self.request = request

    @Cached
    def form(self):
        formdata = getattr(self.request, self.request.method)
        return self.form_class(formdata)


def grant_admin(username):
    profile = user_db.profiles.find_one(username) or {'_id': username}
    profile['is_admin'] = True
    user_db.profiles.save(profile)


def revoke_admin(username):
    profile = user_db.profiles.find_one(username) or {'_id': username}
    profile['is_admin'] = False
    user_db.profiles.save(profile)
