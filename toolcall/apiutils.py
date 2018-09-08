# -*- coding: utf-8 -*-
import re

from .dktoken import Token


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


def dk_token(request):
    return Token(raw_token_from_request(request))


def toolcall_token(request):
    return raw_token_from_request(request)
