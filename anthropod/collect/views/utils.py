from urllib import urlencode
from datetime import datetime

from django.core.urlresolvers import reverse

from anthropod.core import db


def reverse_params(*args, **kwargs):
    '''Call django's reverse function, and append urlencoded 'params'
    onto the end. Note that params have to be passed in as a keyword arg,
    and will clobber any arguments to `reverse` that might have the same name.
    '''
    params = kwargs.pop('params')
    return reverse(*args, **kwargs) + '?' + urlencode(params)


def log_change(request, _id, action):
    '''Super simple change logging.
    '''
    username = request.user.username
    change = dict(
        username=username,
        record_id=_id,
        action=action,
        datetime=datetime.utcnow())
    db.changes.save(change)
