from anthropod.settings.base import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG
SECRET_KEY = '7d05%rr+^+12-v1q%%u$e7=-7-83rxu((n3j3zz9%rit-#xx5q'

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DATABASE = 'ocd'

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INTERNAL_IPS = ('127.0.0.1',)

INSTALLED_APPS += (
    'debug_toolbar',
    'django_extensions')
