# -*- coding: utf-8 -*-

""":mod:`toolcall` views.
"""
import datetime
import json
import os
import time
import traceback

import yaml
from django import http
from django.conf import settings
import dkredis

from . import apiutils
import toolcall.message
from .dktoken import Token

DIRNAME = os.path.dirname(__file__)


def api_definition(request):
    api = yaml.load(open(os.path.join(DIRNAME, 'toolcall-api.yaml')))

    data = json.dumps(api, indent=4, sort_keys=True)
    resp = http.HttpResponse(data, content_type='application/json')
    resp['Content-Type'] = 'application/json; charset=UTF-8'
    return resp


def receive_result(request):
    """This is toolcall informing us that there is a result pending by
       sending an access token which we can exchange for an actual
       result through our side-channel (this was originally a redirect
       of the candidate after end-of-assessment).
    """
    # dkhttp.debug_info(request)
    logfile_name = os.path.join(settings.LOGDIR, 'toolcallresults.log')
    with open(logfile_name, 'a+') as _log:
        logid = int(time.time() * 1000)

        def log(*args):
            print >>_log, logid, datetime.datetime.now(), ' '.join([str(a) for a in args])

        log('starting result transaction')

        try:
            token = apiutils.raw_token_from_request(request)
            log('found token', token)

            r = dkredis.connect()
            rdskey = 'toolcall-token-%s' % token
            if r.get(rdskey) == '1':
                log('already processed:', token)
                return toolcall.message.SuccessResponse(
                    toolcall.message.Message(
                    "ok", token, already_processed=True
                ))
            else:
                # save token for 24 hours
                r.setex(rdskey, 60*60*24, "1")

            log('calling toolcall to fetch result data..')
            result = toolcallresult.fetch_result_token(token, req=request)
            log('got result', result)
            ToolcallResult.store(result)
            log('resultdata successfully stored to db (end).')
            return toolcall.message.SuccessResponse(toolcall.message.Message(
                "ok", token
            ))

        except ValueError as e:
            if str(e) == "Missing token.":
                log('missing token')
                return toolcall.message.ServerError(toolcall.message.Message(
                    "error", None,
                    error="missing-token",
                    msg="Mangler token.",
                ))

            bjorn.traceback(request)
            log('unknown value error', e)
            return toolcall.message.ServerError(toolcall.message.Message(
                "error", token,
                error="value-error",
                msg="Ukjent ValueError.",
            ))

        except:
            # this could be an attack: don't reveal anything..
            bjorn.traceback(request)
            log('unknown error')
            return toolcall.message.ServerError(toolcall.message.Message(
                "error", None,
                error="error",
                msg="Error.",
            ))


def receive_result(request):
    """This is toolcall informing us that there is a result pending by
       sending an access token which we can exchange for an actual
       result through our side-channel (this was originally a redirect
       of the candidate after end-of-assessment).
    """
    token = None
    try:
        token = apiutils.raw_token_from_request(request)
        result = toolcallresult.fetch_result_token(token, req=request)
        ToolcallResult.store(result)
        return toolcall.message.SuccessResponse(toolcall.message.Message(
            "ok", token
        ))

    except ValueError as e:
        # bjorn.traceback(request)
        if str(e) == "Missing token.":
            return toolcall.message.ServerError(toolcall.message.Message(
                "error", None,
                error="missing-token",
                msg="Mangler token.",
            ))
        return toolcall.message.ServerError(toolcall.message.Message(
            "error", token,
            error="value-error",
            msg="Ukjent ValueError.",
        ))

    except:
        # this could be an attack: don't reveal anything..
        # bjorn.traceback(request)
        return toolcall.message.ServerError(toolcall.message.Message(
            "error", None,
            error="error",
            msg="Error.",
        ))


def fetch_token(request):
    """Extract the token from the request, fetch and remove the token's value
       from Redis, and return the value to the client.
    """
    logfile_name = os.path.join(settings.LOGDIR, 'toolcall-fetch-token.log')
    with open(logfile_name, 'a+') as _log:
        logid = int(time.time() * 1000)

        def log(*args):
            print >>_log, logid, datetime.datetime.now(), ' '.join([str(a) for a in args])

        log('toolcall fetching token..')

        token = ""
        try:
            token = toolcall.apiutils.dk_token(request)
            log('found token:', token)
            cn = dkredis.connect()
            pyval = dkredis.pop_pyval('TOKEN-%s' % token, cn)
            log('found value in redis:', pyval)

            if pyval is None:
                return toolcall.message.UnautorizedResponse(
                    toolcall.message.Message(
                    "error", token,
                    error='token-expired',
                    msg='Token finnes ikke.'
                ))

            return toolcall.message.SuccessResponse(pyval)

        except Token.Invalid as e:
            return toolcall.message.UnautorizedResponse(
                toolcall.message.Message(
                "error", token,
                error='token-invalid',
                msg='Token er ugyldig.',
                details=dict(msg=str(e))
            ))

        except Exception as e:
            bjorn.message(request.path, request, traceback.format_exc())
            return toolcall.message.ServerError(toolcall.message.Message(
                "error", token,
                error='unknown-error',
                msg=u'Ukjent feil',
                details=dict(msg=str(e))
            ))

#
# #
# #
# # Debug views
# #
# #


def create_token(request):
    """Debug helper view.

       ========== =====================================================
       Argument   Value
       ========== =====================================================
       timeout    Number of seconds to keep token alive (default=6).
       url        The url to redirect to.
       ========== =====================================================
    """
    token = Token()
    timeout = request.REQUEST.get('timeout', str('6'))
    url = request.REQUEST.get('url', 'https://example.com')
    url += '?access_token=%s' % token

    # usr = request.user
    # usr = User.objects.get(username='xxx')
    value = toolcall.message.Message(
        "person", token,
        firstName="Test",
        lastName="Testesen",
        persnr='12345678901'
    )

    # dkredis.set_pyval('TOKEN-%s' % token, value, timeout)
    # bjorn.message("TOKEN:", token)
    return http.HttpResponseRedirect(url)
