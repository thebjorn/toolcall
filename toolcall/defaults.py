# -*- coding: utf-8 -*-
from django.conf import settings


def _get(attr, default=None):
    return getattr(settings, attr, default)

if settings.DEBUG:
    TOOLCALL_TOKEN_TIMEOUT_SECS = 200
else:
    TOOLCALL_TOKEN_TIMEOUT_SECS = _get('TOOLCALL_TOKEN_TIMEOUT_SECS', 10)

TOOLCALL_TOKEN_SIZE = _get('TOOLCALL_TOKEN_SIZE', 51)
TOOLCALL_ERROR_RESTART_URL = _get('TOOLCALL_ERROR_RESTART_URL', "https://www.finaut.no/")
TOOLCALL_SERVICE_ROOT_URL = _get('TOOLCALL_SERVICE_ROOT_URL', "https://afr.norsktest.no/toolcall/")

TOOLCALL_START_URL = 'starturl'
TOOLCALL_STAGING_START_URL = 'starturl'
TOOLCALL_SUCCESS_URL = _get('TOOLCALL_SUCCESS_URL', "http://www.autorisasjonsordningen.no/profile/")
TOOLCALL_FAIL_URL = _get('TOOLCALL_FAIL_URL', "http://www.autorisasjonsordningen.no/profile/")

TOOLCALL_RENEW_TOKEN_URL = 'renew-token-url'
TOOLCALL_STAGING_RESULT_DATA = 'staging-result-data'
