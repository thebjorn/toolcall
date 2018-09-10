# -*- coding: utf-8 -*-
import datetime
import random

import requests
from django import http

# (http://localhost:8000/.api/toolcall/v2/) api.urls.root-url
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import dkredis

import toolcall

SERVER_ROOT_URL = "http://localhost:8000/"

# (http://localhost:8000/.api/toolcall/v2/) api.urls.start_data.url
START_DATA_URL = 'fetch-token/'

# (http://localhost:8000/.api/toolcall/v2/) api.urls.result_token.url
RESULT_TOKEN_URL = 'result/'


def receive_start_token(request):
    token = request.REQUEST['access_token']
    # check if token has been seen before..?
    url = SERVER_ROOT_URL + START_DATA_URL + '?access_token=' + token

    # return token and get start data
    r = requests.get(url)
    start_data = r.json()

    if start_data['type'] == 'error':
        # display errors to user (with token) if you can't handle the error
        # in a reasonable fashion
        return http.HttpResponse("ERROR (%s): %s<br>(%s)" % (
            start_data['data']['error'],
            start_data['data']['msg'],
            start_data['token']
        ))

    # Note: you have to return start_data['system'] with your result data.
    #       Here I log the user in and save it in their session, there are
    #       probably other/better ways to do this.

    username = start_data['data']['persnr']
    # create user if new
    if not User.objects.filter(username=username):
        User.objects.create(
            username=username,
            first_name=start_data['data']['firstName'],
            last_name=start_data['data']['lastName'],
        )

    # this authenticate should end up in
    # toolcall.auth_backend.DKSSOBlindTrustAuthenticator
    # (you can also "cheat" by setting user.backend directly insted..)
    user = authenticate(username=start_data['data']['persnr'], sso_login=True)
    login(request, user)

    request.session['start-data'] = start_data
    return http.HttpResponseRedirect('/client/start-exam/my-tool/')


def run_my_tool(request):
    # run exam..
    # using a random value here to demonstrate that this token is
    # generated on the client
    token = str(random.randrange(2**16, 2**32))

    start = request.session['start-data']['data']
    result = {
        'token': token,
        'type': 'result',
        'timestamp': datetime.datetime.now().isoformat(),
        'data': {
            'persnr': start['persnr'],
            'participant_id': 42,      # client-local ID
            'exam': start['exam'],  # (my-tool)
            'passed': True,         # did the user pass the test
            "score": 42,
            "system": start['system'],
            "exam_type": start["exam_kind"]  # historical accident..
        }
    }
    dkredis.set_pyval('CLIENT-TOKEN-' + token,
                      result,
                      200)  # seconds

    url = SERVER_ROOT_URL + RESULT_TOKEN_URL
    url += '?access_token=' + token
    url += '&client=testclient'  # must match Client.name
    print "REDIRECTING TO: ", url

    return http.HttpResponseRedirect(url)


def send_result_data(request):
    print "in send-result-data:", request.GET
    result = dkredis.pop_pyval("CLIENT-TOKEN-" + request.GET['access_token'])
    print "CLIENT_RESULT:", result
    return toolcall.message.SuccessResponse(
        result
    )
