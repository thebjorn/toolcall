# -*- coding: utf-8 -*-
from django.conf import settings


def _default(attr, default=None):
    globals()[attr] = getattr(settings, attr, default)


_default('TOOLCALL_TOKEN_TIMEOUT_SECS', 1)
_default('TOOLCALL_TOKEN_SIZE', 51)
_default('TOOLCALL_ERROR_RESTART_URL', 'https://www.finaut.no/')
_default('TOOLCALL_SERVICE_ROOT_URL', "https://afr.norsktest.no/toolcall/")
_default('TOOLCALL_SUCCESS_URL', "http://www.autorisasjonsordningen.no/profile/")
_default('TOOLCALL_FAIL_URL', "http://www.autorisasjonsordningen.no/profile/")
