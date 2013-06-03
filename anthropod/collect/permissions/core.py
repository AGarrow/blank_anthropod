import logging

from django.core.exceptions import PermissionDenied
from django.conf import settings

from anthropod.core import user_db


logger = logging.getLogger(__name__)


def check_permissions(request, ocd_id, *permissions):
    '''Check whether the request.user has the specified permissions;
    if not, raise PermissionDenied.
    '''
    # Skip permissions check for admins.
    for _, email in settings.ADMINS:
        if email == request.user.email:
            return

    spec = {
        'username': request.user.username,
        'ocd_id': ocd_id,
        'permissions': {'$all': permissions},
        }

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
    spec = {
        'username': username,
        'ocd_id': ocd_id,
        }
    document = {
        '$pullAll': {'permissions': permissions}
        }
    user_db.permissions.update(spec, document, upsert=True, multi=True)
    args = (username, permissions)
    logger.info('Revoked the following permissions from %r: %r' % args)

