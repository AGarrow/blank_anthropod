from anthropod.settings.local import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG

# This has to be set in order for template.DEBUG to be true.
INTERNAL_IPS = ('127.0.0.1',)

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DATABASE = 'ocd'

