# try:
#   from anthropod.settings.base import *
from anthropod.settings.local import *
# except ImportError:
#   pass

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# This has to be set in order for template.DEBUG to be true.
INTERNAL_IPS = ('127.0.0.1',)

INSTALLED_APPS += ('django_nose',)

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DATABASE = 'pupa'
MONGO_USER_DATABASE = 'placeholder'

try:
  LOGGING
except NameError:
  LOGGING={}


# Add some extra dev logging.
LOGGING['formatters']['verbose'] = {
    'format': '[%(asctime)s] %(name)s: %(message)s'
    }

LOGGING['handlers']['console'] = {
    'level': 'DEBUG',
    'class': 'logging.StreamHandler',
    'formatter': 'verbose',
    }

LOGGING['loggers']['locust.client'] = {
    'handlers': ['console'],
    'level': 'DEBUG',
    }
