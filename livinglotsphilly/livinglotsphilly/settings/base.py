import os
from os.path import abspath, dirname

from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    """Get the environment variable or return exception"""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s env variable" % var_name
        raise ImproperlyConfigured(error_msg)

DATABASES = {
    'default': {
        # > createdb -T template_postgis philly_living_lots
        # > psql
        # # create user philly_living_lots with password 'password';
        # # grant all privileges on database philly_living_lots to
        # philly_living_lots;
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': get_env_variable('PHILLY_DB_NAME'),
        'USER': get_env_variable('PHILLY_DB_USER'),
        'PASSWORD': get_env_variable('PHILLY_DB_PASSWORD'),
        'HOST': get_env_variable('PHILLY_DB_HOST'),
        'PORT': get_env_variable('PHILLY_DB_PORT'),
    }
}

gettext = lambda s: s

LANGUAGES = (
    ('en', gettext('English')),
    ('es', gettext('Spanish')),
)

LANGUAGE_CODE = 'en'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True
TIME_ZONE = 'America/New_York'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

PROJECT_ROOT = os.path.join(abspath(dirname(__file__)), '..', '..')

DATA_ROOT = os.path.join(PROJECT_ROOT, '..', 'data')

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'collected_static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = get_env_variable('PHILLY_SECRET_KEY')

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'honeypot.middleware.HoneypotMiddleware',
    'reversion.middleware.RevisionMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',

    'feincms.context_processors.add_page_if_missing',

    'lots.context_processors.map_tile_urls',
)

ROOT_URLCONF = 'livinglotsphilly.urls'

WSGI_APPLICATION = 'livinglotsphilly.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',

    #
    # django contrib
    #
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.webdesign',

    #
    # third-party
    #
    'actstream',
    'admin_enhancer',
    'autocomplete_light',
    'chosen',
    'contact_form',
    'django_monitor',
    'djangojs',
    'elephantblog',
    'feincms',
    'feincms.module.medialibrary',
    'feincms.module.page',
    'flatblocks',
    'forms_builder.forms',
    'honeypot',
    'imagekit',
    'inplace',
    'inplace.boundaries',
    'jsonfield',
    'mptt',
    'report_builder',
    'reversion',
    'reversion_compare',
    'widget_tweaks',

    #
    # first-party, project-generic
    #
    'external_data_sync',
    'inplace_activity_stream',
    'livinglots_flatblockspreview',
    'livinglots_mailings',
    'livinglots_organize',
    'livinglots_usercontent.files',
    'livinglots_usercontent.notes',
    'livinglots_usercontent.photos',
    'libapps.facebook',
    'libapps.twitter',
    'phillydata',
    'phillydata.availableproperties',
    'phillydata.citycouncil',
    'phillydata.landuse',
    'phillydata.li',
    'phillydata.licenses',
    'phillydata.opa',
    'phillydata.owners',
    'phillydata.parcels',
    'phillydata.taxaccounts',
    'phillydata.violations',
    'phillydata.waterdept',
    'phillydata.zoning',

    #
    # first-party, project-specific
    #
    'activity_stream',
    'blog',
    'cms',
    'contact',
    'extraadmin',
    'groundtruth',
    'lots',
    'mailreader',
    'pathways',
    'phillydata_local',
    'phillyorganize',
    'steward',
    'survey',
)

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
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

PLACES_MAPBOX_ID = 'amylaura.i1003357'

SOUTH_TESTS_MIGRATE = False

RECAPTCHA_PRIVATE_KEY = get_env_variable('PHILLY_RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_PUBLIC_KEY = get_env_variable('PHILLY_RECAPTCHA_PUBLIC_KEY')

ORGANIZE_PARTICIPANT_SALT = get_env_variable('PHILLY_ORGANIZE_PARTICIPANT_SALT')

ACTSTREAM_SETTINGS = {
    'MANAGER': 'inplace_activity_stream.managers.PlaceActionManager',
}
ACTIVITY_STREAM_DEFAULT_ACTOR_PK = get_env_variable('PHILLY_ACTSTREAM_DEFAULT_ACTOR_PK')

FACILITATORS = {
    'global': [],
}

EMAIL_SUBJECT_PREFIX = '[Grounded in Philly] '

MAILREADER_REPLY_PREFIX = 'Reply with text above this line to post a public note.'
MAILREADER_IGNORE_FROM = []
MAILREADER_HOST = get_env_variable('PHILLY_MAILREADER_HOST')
MAILREADER_HOST_USER = get_env_variable('PHILLY_MAILREADER_HOST_USER')
MAILREADER_HOST_PASSWORD = get_env_variable('PHILLY_MAILREADER_HOST_PASSWORD')

FEINCMS_RICHTEXT_INIT_CONTEXT = {
    'TINYMCE_JS_URL': STATIC_URL + 'bower_components/tinymce/tinymce.min.js',
}

def elephantblog_entry_url_app(self):
    from feincms.content.application.models import app_reverse
    return app_reverse('elephantblog_entry_detail', 'elephantblog.urls',
                       kwargs={
                           'year': self.published_on.strftime('%Y'),
                           'month': self.published_on.strftime('%m'),
                           'day': self.published_on.strftime('%d'),
                           'slug': self.slug,
                       })


def elephantblog_categorytranslation_url_app(self):
    from feincms.content.application.models import app_reverse
    return app_reverse('elephantblog_category_detail', 'elephantblog.urls',
                       kwargs={ 'slug': self.slug, })


def pathways_pathway_url_app(self):
    from feincms.content.application.models import app_reverse
    return app_reverse('pathway_detail', 'pathways.urls', kwargs={
        'slug': self.slug,
    })


ABSOLUTE_URL_OVERRIDES = {
    'elephantblog.entry': elephantblog_entry_url_app,
    'elephantblog.categorytranslation': elephantblog_categorytranslation_url_app,
}

HONEYPOT_FIELD_NAME = 'homepage'
HONEYPOT_VALUE = 'http://example.com/'

LOT_MAP_TILE_URLS = {}

ORGANIZE = {
    'ORGANIZER_MODEL': 'phillyorganize.Organizer',
}

ADMIN_TOOLS_INDEX_DASHBOARD = 'livinglotsphilly.admindashboard.PhillyDashboard'

CONSTANT_CONTACT_API_KEY = get_env_variable('PHILLY_CONSTANT_CONTACT_API_KEY')
CONSTANT_CONTACT_LIST = get_env_variable('PHILLY_CONSTANT_CONTACT_LIST')
CONSTANT_CONTACT_TOKEN = get_env_variable('PHILLY_CONSTANT_CONTACT_TOKEN')

LIVING_LOTS = {
    'MODELS': {
        'organizer': 'phillyorganize.Organizer',
    },
}
