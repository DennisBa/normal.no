# https://docs.djangoproject.com/en/1.5/ref/settings/


# Find full path to Djang's root folder.
import os.path
tmp = os.path.dirname (os.path.abspath (__file__))
tmp = os.path.join (tmp, '..', '..')
ROOT = os.path.realpath (tmp)


# Private settings that should *not* go inside a public repository!
import website.settings_local as local


##
## Custom settings (not used by Django)
##

# FILE_UPLOAD_MAX_SIZE = "5242880"




##
## Django settings
##

DEBUG = True
TEMPLATE_DEBUG = DEBUG

INTERNAL_IPS = local.INTERNAL_IPS

ADMINS = local.ADMINS
MANAGERS = local.MANAGERS

DATABASES = local.DATABASES

SECRET_KEY = local.SECRET_KEY


FILE_UPLOAD_PERMISSIONS = 0644
# FILE_UPLOAD_MAX_MEMORY_SIZE   # 2.5M

# contrib.auth
AUTH_PROFILE_MODULE = 'users.profile'
#LOGIN_URL = '/users/login'
#LOGIN_REDIRECT_URL     # default: /accounts/profile/

TIME_ZONE = 'Europe/Oslo'       # None => /etc/timezone

#LANGUAGE_CODE = 'en-us'         # XXX used for what??
LANGUAGE_CODE = 'nb-no'
# django.utils.translation.to_locale
# Turns a language name (en-us) into a locale name (en_US).

# contrib.site (required by contrib.flatpages)
SITE_ID = 1

USE_I18N = False
#USE_I18N = True

# Format according to the current locale.
USE_L10N = False
#USE_L10N = True

# UPDATE: USE_I18N=True & LANGUAGE_CODE to format dates!
# TODO but only want date/number formating, not translations! how?

# Use timezone-aware datetimes?
USE_TZ = False

# Absolute filesystem path to store user-uploaded files.
# TODO rename upload?
MEDIA_ROOT = os.path.join (ROOT, 'django', 'htdocs', 'media')

# URL of MEDIA_ROOT. Must be mapped by webserver.
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
STATIC_ROOT = os.path.join (ROOT, 'django', 'htdocs', 'static')

# URL of STATIC_ROOT. Must be mapped by webserver.
STATIC_URL = '/static/'

# Global (non-app) static files.
STATICFILES_DIRS = (
    os.path.join (ROOT, 'django', 'static'),    # static/{css,js,images}
    # TODO split out binary files?
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


TEMPLATE_DIRS = (
    os.path.join (ROOT, 'django', 'templates'),
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # TODO if not DEBUG:
    #   django.template.loaders.cached.Loader
)

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.debug',
)


# Note: these are invoked in reverse order for the response.
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
        # note: flatpages should be last.
)


ROOT_URLCONF = 'website.urls'

WSGI_APPLICATION = 'website.wsgi.application'


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.flatpages',
    # 'django.contrib.admindocs',

    'core',
    'apps.news',
    'apps.links',
)


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
