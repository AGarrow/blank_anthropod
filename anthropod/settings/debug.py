from anthropod.settings.dev import *


MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INTERNAL_IPS = ('127.0.0.1',)

# For emergencias, debug middleware breaks into pdb early in every request.
INSTALLED_APPS = ('debug_middleware.DebugMiddleWare',) += INSTALLED_APPS
INSTALLED_APPS += (
    'debug_toolbar',
    'django_extensions')

