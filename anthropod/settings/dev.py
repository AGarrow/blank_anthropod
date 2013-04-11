from anthropod.settings.local import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG

# This has to be set in order for template.DEBUG to be true.
INTERNAL_IPS = ('127.0.0.1',)

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DATABASE = 'ocd'

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
