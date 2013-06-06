from os.path import abspath, dirname, join


PROJECT_ROOT = abspath(join(dirname(__file__), '..'))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('James Turk', 'jturk@sunlightfoundation.com'),
    ('Thom Neale', 'tneale@sunlightfoundation.com'),
    ('Thom Neale', 'twneale@gmail.com'),
    ('Paul Tagliamonte', 'paultag@sunlightfoundation.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(PROJECT_ROOT, 'anthropod.sqlite3'),
    }
}

ALLOWED_HOSTS = []

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = ''
MEDIA_URL = ''

STATIC_ROOT = join(PROJECT_ROOT, '..', 'collected_static')
STATIC_URL = '/media/'

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',

)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'anthropod.urls'

WSGI_APPLICATION = 'anthropod.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'locksmith.mongoauth',
    'social_auth',
    'anthropod.collect',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


AUTHENTICATION_BACKENDS = (
    'sunlightauth.backends.SunlightBackend',
    #'django.contrib.auth.backends.ModelBackend',
)

SUNLIGHT_AUTH_BASE_URL = 'http://login.sunlightfoundation.com/'
# SUNLIGHT_AUTH_APP_ID = 'anthropod'
SUNLIGHT_AUTH_APP_ID = 'openstates'
#SUNLIGHT_AUTH_SECRET = 'set in local settings'
SUNLIGHT_AUTH_SCOPE = []

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/sunlight/'

LOCKSMITH_REGISTRATION_URL = 'http://services.sunlightlabs.com/accounts/register/'
