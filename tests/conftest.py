# -*- coding: utf-8 -*-
import os

import django

DIRNAME=os.path.dirname(__file__)
# os.environ['DJANGO_SETTINGS_MODULE'] = 'finautapi.settings'   # same as dkbuild.ini

def pytest_configure():

    from django.conf import settings
    settings.configure(
        DEBUG=True,
        TESTING=True,
        PRODUCTION=False,
        # DKCSRF_COOKIE_NAME="csrftoken",
        ROOT_URLCONF='urls',
        APPNAME='toolcall',
        CACHES={
            'default': {
                'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
                'LOCATION': os.path.join(os.environ['SRV'], 'data', 'cache'),
                'TIMEOUT': 60 * 60,
                'OPTIONS': {
                    'MAX_ENTRIES': 5000
                }
            }
        },
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
                'NAME': os.path.join(DIRNAME, 'testing.db'),  # Or path to database file if using sqlite3.
                # The following settings are not used with sqlite3:
                'USER': '',
                'PASSWORD': '',
                'HOST': '',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
                'PORT': '',  # Set to empty string for default.
            }
        },
        INSTALLED_APPS=(
            # 'django_extensions',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.admin',
            'django.contrib.sites',
            'django.contrib.staticfiles',
            'requests',
            'dateutil',
            # 'dk',
            # 'dksys',
            # 'dkdjango',
            # 'dkjs',
            'toolcall'
        ),
    )
    django.setup()
