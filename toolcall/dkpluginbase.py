# -*- coding: utf-8 -*-
import pprint
import uuid
import datetime
from dkdjango import dkhttp
from toolcall.defaults import TOOLCALL_RENEW_TOKEN_URL
from django import http
from dkjs import jason
import re


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


def raw_token_from_request(request):
    try:
        access_token = request.REQUEST.get(
            'access_token',
            request.META.get('HTTP_X_ACCESS_TOKEN'))
        if access_token is None:
            auth = request.META.get('Authorization')
            if not auth:
                raise ValueError("Missing token.")
            # XXX: the following is incorrect, it should be
            # XXX: Token {{token:auth}.encode(base64)[:-1]}
            m = re.match(r'Token token="([^"]+)"', auth)
            if not m:
                print 'handle authorization fail'
            access_token = m.groups(1)
        return str(access_token)
    except ValueError:
        # do we want to do anything here..?
        raise


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

