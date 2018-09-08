# -*- coding: utf-8 -*-
import datetime
import os
import time

from django import http
from django.conf import settings

import toolcall.message
from toolcall import apiutils
from toolcall.dktoken import Token


def fetch_start_token(request):
    """Fetch data from the token that the calling site deposited in redis.
    """
    startinfo = {}
    try:
        starttoken = apiutils.dk_token(request)
        cn = dkredis.connect()
        startinfo = dkredis.pop_pyval('TOKEN-%s' % starttoken, cn)

        if startinfo is None:
            # bjorn.message(request.path, request, "starttoken-expired")
            return None

        return startinfo

    except Token.Invalid as e:
        # bjorn.message(request.path, request, traceback.format_exc())
        return None

    except Exception as e:
        # bjorn.message(request.path, request, traceback.format_exc())
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
        value = toolcall.message.Message(
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
