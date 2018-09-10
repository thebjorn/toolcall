# -*- coding: utf-8 -*-
import datetime
import pprint
import uuid

from django import http

from . import dkhttp, jason
from .defaults import TOOLCALL_RENEW_TOKEN_URL


class Message(object):
    """Convenience class that holds message data and can convert it to json.
    """

    def __init__(self, kind, token, **data):
        self.type = kind
        self.msgid = str(uuid.uuid1())
        self.token = str(token)
        self.timestamp = datetime.datetime.now().isoformat()
        self.data = data

    def __str__(self):
        return pprint.pformat(self.__dict__)

    def __json__(self):
        return self.__dict__


def UnautorizedResponse(msg):
    """Return a 401 response with a json encoded error message.
       Also sets the `WWW-Authenticate` header, giving an appropriate
       url for users to restart the process (TOOLCALL_RENEW_TOKEN_URL).
    """
    response = dkhttp.HttpUnauthorized(jason.dumps(msg))
    response['Content-Type'] = 'application/json'
    auth_url = 'Token realm="Person", location="%s"' % TOOLCALL_RENEW_TOKEN_URL
    response['WWW-Authenticate'] = auth_url
    return response


def SuccessResponse(msg):
    """Return a 200 response with a json encoded message.
    """
    response = http.HttpResponse(jason.dumps(msg))
    response['Content-Type'] = 'application/json'
    return response


def ServerError(msg):
    """Return a 500 response with a json encoded message.
    """
    response = http.HttpResponseServerError(jason.dumps(msg))
    response['Content-Type'] = 'application/json'
    return response
