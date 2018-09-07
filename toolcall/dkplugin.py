# -*- coding: utf-8 -*-

from django.conf import settings
from dkdjango.dktoken import Token
from toolcall.defaults import (
    TOOLCALL_START_URL, TOOLCALL_RESULT_DATA, TOOLCALL_STAGING_START_URL,
    TOOLCALL_STAGING_RESULT_DATA
)
from toolcall.cls2pset import pset, PluginBase
from toolcall.dkpluginbase import *  # extends interface


def dk_token(request):
    return Token(raw_token_from_request(request))


def toolcall_token(request):
    return raw_token_from_request(request)


def serviceurl(url):
    return TOOLCALL_SERVICE_ROOT_URL + url


class ServiceUrl(pset):
    def __init__(self, url, description):
        super(ServiceUrl, self).__init__()
        self.url = url
        self.description = u' '.join(description.split())


class toolcall_plugin(PluginBase):
    type = 'external-assessment'
    name = 'toolcall'
    version = 1
    if settings.DEBUG:
        timeout = 200
    else:  # pragma: nocover
        timeout = 6

    class person:
        "Exchange token for person data."
        url = serviceurl("fetch-token/")

    class assessment_begin:
        """Authenticate and authorize user, before redirecting them with
           a token.
        """
        url = serviceurl("assessment-begin/")

    class assessment_done:
        """Receive redirect after user has finished
           assessment with a token to fetch the result.
        """
        url = serviceurl("result/")
        success = defaults.TOOLCALL_SUCCESS_URL       # redirect here if success
        fail = defaults.TOOLCALL_SUCCESS_URL             # redirect here if fail

    class assessment_redirect:
        """Redirect authenticated and authorized user with a token.
        """
        if settings.DEBUG:
            url = TOOLCALL_STAGING_START_URL
        else:  # pragma: nocover
            url = TOOLCALL_START_URL

    class result:
        "Exchange token for result data."
        if settings.DEBUG:
            url = TOOLCALL_STAGING_RESULT_DATA
        else:  # pragma: nocover
            url = TOOLCALL_RESULT_DATA


if __name__ == "__main__":  # pragma: nocover
    import json
    print json.dumps(toolcall_plugin, indent=4, sort_keys=True)
