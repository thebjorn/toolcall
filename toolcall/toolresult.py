# -*- coding: utf-8 -*-

"""Base level handling of results from toolcall.
"""
import requests

from toolcall import jsondecoder
from toolcall.toolcall_exceptions import (
    ToolcallJSonDecodeError,
    ToolcallResultException,
    ToolcallMessageException,
    ToolcallInvalidResponse)
from dk.collections import pset


def fetch_result_token(client, token):
    """Return validated data from toolcall result token.
    """
    try:
        # res = requests.get(
        #     client.receive_result_token_url,
        #     headers={'Accept': 'application/json,text/*'},
        #     data={'access_token': str(token)}
        # )
        res = requests.get(client.receive_result_token_url + '?access_token=' + str(token))
        if not res.ok:
            raise ToolcallInvalidResponse(
                "Not a 200 response: %r, token: %r" % (res, token))
    except requests.RequestException:
        # bjorn.traceback()
        raise

    try:
        result = jsondecoder.loads(res.text)
    except ValueError as e:
        raise ToolcallJSonDecodeError(str(e))

    if not isinstance(result, pset):
        raise ToolcallJSonDecodeError(
            "Returned value was not a result but a %r (%s)" % (
                result, type(result)))

    if not hasattr(result, 'token'):
        raise ToolcallResultException("Missing token in result: %r" % result)

    if result.token != token:
        raise ToolcallResultException(
            "Result has unexpected token. Expected: %r, got %r\n%r" % (
                token, result.token, result))

    return validate_result_data(result)


def _verify_attr(msg, attr):
    """Verify that message `msg` has attribute `attr` or throw an exception.
    """
    if not hasattr(msg, attr):
        raise ToolcallMessageException(
            "Message missing '%s' attribute: %r" % (attr, msg)
        )


def validate_message(m):
    """Validate message structure.
    """
    _verify_attr(m, 'type')
    _verify_attr(m, 'timestamp')
    _verify_attr(m, 'data')
    return m


def validate_result_data(r):
    """Validate the structure `r` as a valid result.
    """
    validate_message(r)
    data = r.data
    if hasattr(data, 'participation_id'):
        data.participant_id = data.participation_id
    _verify_attr(data, 'persnr')
    _verify_attr(data, 'participant_id')
    _verify_attr(data, 'exam')
    _verify_attr(data, 'passed')
    _verify_attr(data, 'score')
    _verify_attr(data, 'system')
    _verify_attr(data, 'exam_type')
    return r
