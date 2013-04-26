from urllib import urlencode

from django.core.urlresolvers import reverse


def reverse_params(*args, **kwargs):
    '''Call django's reverse function, and append urlencoded 'params'
    onto the end. Note that params have to be passed in as a keyword arg,
    and will clobber any arguments to `reverse` that might have the same name.
    '''
    params = kwargs.pop('params')
    return reverse(*args, **kwargs) + '?' + urlencode(params)
