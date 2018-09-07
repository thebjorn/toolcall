# -*- coding: utf-8 -*-

""":mod:`toolcall` views.
"""
import datetime
import os
import time
import traceback

from django import http
from django.conf import settings

from dkdjango import dkhttp
from dkdjango.dktoken import Token
from dkjs import jason
from dksys import dkredis, bjorn
from finautlogin.decorators import finaut_sso_required

from toolcall import defaults
from . import dkplugin, toolcallresult
from .dkplugin import toolcall_plugin
from .models import ToolcallResult


@finaut_sso_required
def plugin_definition(request):
    return jason.response(request, toolcall_plugin)


def fetch_start_token(request):
    """Fetch data from the token that the calling site deposited in redis.
    """
    startinfo = {}
    try:
        starttoken = dkplugin.dk_token(request)
        cn = dkredis.connect()
        startinfo = dkredis.pop_pyval('TOKEN-%s' % starttoken, cn)

        if startinfo is None:
            bjorn.message(request.path, request, "starttoken-expired")
            return None

        return startinfo

    except Token.Invalid as e:
        bjorn.message(request.path, request, traceback.format_exc())
        return None

    except Exception as e:
        bjorn.message(request.path, request, traceback.format_exc())
        return None


def assessment_begin(request):
    """Authenticate and authorize user, before redirecting them with
       a token.
    """
    startinfo = fetch_start_token(request)
    if startinfo is None:
        url = defaults.TOOLCALL_ERROR_RESTART_URL
        return http.HttpResponseRedirect(url)

    logfile_name = os.path.join(settings.LOGDIR, 'toolcall-begin-assessment.log')
    with open(logfile_name, 'a+') as _log:
        logid = int(time.time() * 1000)

        def log(*args):
            print >>_log, logid, datetime.datetime.now(), ' '.join([str(a) for a in args])

        token = Token()
        timeout = toolcall_plugin.timeout
        url = toolcall_plugin.assessment_redirect.url
        url += '?access_token=%s' % token

        usr = request.user
        value = dkplugin.Message(
            "person", token,
            firstName=startinfo['first_name'],
            lastName=startinfo['last_name'],
            exam=startinfo['exam'],
            persnr=startinfo['persnr'],
            extra_time=startinfo['extra_time'],
            exam_kind=startinfo['exam_kind'],
            redirect_url=startinfo['redirect_url'],
            system=startinfo['system']
        )

        dkredis.set_pyval('TOKEN-%s' % token, value, timeout)
        log('sending to toolcall:', token, value)
        return http.HttpResponseRedirect(url)


def receive_result(request):
    """This is toolcall informing us that there is a result pending by
       sending an access token which we can exchange for an actual
       result through our side-channel (this was originally a redirect
       of the candidate after end-of-assessment).
    """
    dkhttp.debug_info(request)
    logfile_name = os.path.join(settings.LOGDIR, 'toolcallresults.log')
    with open(logfile_name, 'a+') as _log:
        logid = int(time.time() * 1000)

        def log(*args):
            print >>_log, logid, datetime.datetime.now(), ' '.join([str(a) for a in args])

        log('starting result transaction')

        try:
            token = dkplugin.toolcall_token(request)
            log('found token', token)

            r = dkredis.connect()
            rdskey = 'toolcall-token-%s' % token
            if r.get(rdskey) == '1':
                log('already processed:', token)
                return dkplugin.SuccessResponse(dkplugin.Message(
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
            return dkplugin.SuccessResponse(dkplugin.Message(
                "ok", token
            ))

        except ValueError as e:
            if str(e) == "Missing token.":
                log('missing token')
                return dkplugin.ServerError(dkplugin.Message(
                    "error", None,
                    error="missing-token",
                    msg="Mangler token.",
                ))

            bjorn.traceback(request)
            log('unknown value error', e)
            return dkplugin.ServerError(dkplugin.Message(
                "error", token,
                error="value-error",
                msg="Ukjent ValueError.",
            ))

        except:
            # this could be an attack: don't reveal anything..
            bjorn.traceback(request)
            log('unknown error')
            return dkplugin.ServerError(dkplugin.Message(
                "error", None,
                error="error",
                msg="Error.",
            ))

# def receive_result(request):
#     """This is toolcall informing us that there is a result pending by
#        sending an access token which we can exchange for an actual
#        result through our side-channel (this was originally a redirect
#        of the candidate after end-of-assessment).
#     """
#     token = None
#     try:
#         token = dkplugin.toolcall_token(request)
#         result = toolcallresult.fetch_result_token(token, req=request)
#         ToolcallResult.store(result)
#         return dkplugin.SuccessResponse(dkplugin.Message(
#             "ok", token
#         ))
#
#     except ValueError as e:
#         bjorn.traceback(request)
#         if str(e) == "Missing token.":
#             return dkplugin.ServerError(dkplugin.Message(
#                 "error", None,
#                 error="missing-token",
#                 msg="Mangler token.",
#             ))
#         return dkplugin.ServerError(dkplugin.Message(
#             "error", token,
#             error="value-error",
#             msg="Ukjent ValueError.",
#         ))
#
#     except:
#         # this could be an attack: don't reveal anything..
#         bjorn.traceback(request)
#         return dkplugin.ServerError(dkplugin.Message(
#             "error", None,
#             error="error",
#             msg="Error.",
#         ))


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
            token = dkplugin.dk_token(request)
            log('found token:', token)
            cn = dkredis.connect()
            pyval = dkredis.pop_pyval('TOKEN-%s' % token, cn)
            log('found value in redis:', pyval)

            if pyval is None:
                return dkplugin.UnautorizedResponse(dkplugin.Message(
                    "error", token,
                    error='token-expired',
                    msg='Token finnes ikke.'
                ))

            return dkplugin.SuccessResponse(pyval)

        except Token.Invalid as e:
            return dkplugin.UnautorizedResponse(dkplugin.Message(
                "error", token,
                error='token-invalid',
                msg='Token er ugyldig.',
                details=dict(msg=str(e))
            ))

        except Exception as e:
            bjorn.message(request.path, request, traceback.format_exc())
            return dkplugin.ServerError(dkplugin.Message(
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
#
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
    value = dkplugin.Message(
        "person", token,
        firstName="Test",
        lastName="Testesen",
        persnr='12345678901'
    )

    dkredis.set_pyval('TOKEN-%s' % token, value, timeout)
    # bjorn.message("TOKEN:", token)
    return http.HttpResponseRedirect(url)
