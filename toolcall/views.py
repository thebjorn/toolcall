# -*- coding: utf-8 -*-

""":mod:`toolcall` views.
"""
import json
import os
import traceback

import yaml
from django import http, shortcuts as dj, template
import dkredis

from toolcall import toolresult
from . import apiutils
from .models import Tool, ToolCall, Client
import toolcall.message
from .dktoken import Token

DIRNAME = os.path.dirname(__file__)


def home(request):
    return dj.render_to_response('toolcall/home.html', template.Context({
        "tools": Tool.objects.all()
    }))


def api_definition(request):
    api = yaml.load(open(os.path.join(DIRNAME, 'toolcall-api.yaml')))

    data = json.dumps(api, indent=4, sort_keys=True)
    resp = http.HttpResponse(data, content_type='application/json')
    resp['Content-Type'] = 'application/json; charset=UTF-8'
    return resp


def fetch_token(request):
    """Extract the token from the request, fetch and remove the token's value
       from Redis, and return the value to the client.
    """
    token = ""
    try:
        token = toolcall.apiutils.dk_token(request)
        # log('found token:', token)
        pyval = dkredis.pop_pyval('TOKEN-%s' % token)
        # log('found value in redis:', pyval)
        print "PYVAL:", pyval

        if pyval is None:
            return toolcall.message.UnautorizedResponse(
                toolcall.message.Message(
                "error", token,
                error='token-expired',
                msg='Token finnes ikke.'  # Token does not exist
            ))

        progress = ToolCall.get(pyval.data['system'])
        progress.set_status('result-tk-sent')
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
        traceback.print_exc()
        # bjorn.message(request.path, request, traceback.format_exc())
        return toolcall.message.ServerError(toolcall.message.Message(
            "error", token,
            error='unknown-error',
            msg=u'Ukjent feil',
            details=dict(msg=str(e))
        ))


def receive_result(request):
    """This is toolcall informing us that there is a result pending by
       sending an access token which we can exchange for an actual
       result through our side-channel (this was originally a redirect
       of the candidate after end-of-assessment).
    """
    token = None
    client = dj.get_object_or_404(Client, name=request.GET['client'])
    try:

        token = apiutils.raw_token_from_request(request)
        result = toolresult.fetch_result_token(client, token)
        progress = ToolCall.get(result.data.system)
        progress.finished_ok()
        print "RECEIVED:RESULT:", result
        # ToolcallResult.store(result)
        return toolcall.message.SuccessResponse(toolcall.message.Message(
            "ok", token
        ))

    except ValueError as e:
        # raise
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
        # raise
        # this could be an attack: don't reveal anything..
        return toolcall.message.ServerError(toolcall.message.Message(
            "error", None,
            error="error",
            msg="Error.",
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
