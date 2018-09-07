# -*- coding: utf-8 -*-
import json

import pytest
from django.test import RequestFactory
from dkdjango.dktoken import Token
from dkjs import jason
from toolcall import jsondecoder
from toolcall.dkplugin import toolcall_plugin
from toolcall.dkpluginbase import Message, SuccessResponse, ServerError, raw_token_from_request
from toolcall.dkpluginbase import UnautorizedResponse


def test_message():
    msg = Message('kind', Token(), hello='world')
    out = jsondecoder.loads(jason.dumps(msg))
    assert out['type'] == msg.type
    assert out['msgid'] == msg.msgid
    assert out['token'] == msg.token
    assert out['timestamp'].isoformat() == msg.timestamp
    assert dict(out['data']) == msg.data


def test_responses():
    msg = Message('kind', Token(), hello='world')

    r = UnautorizedResponse(msg)
    assert r.status_code == 401

    r = SuccessResponse(msg)
    assert r.status_code == 200

    r = ServerError(msg)
    assert r.status_code == 500


def test_raw_token_from_request():
    with pytest.raises(ValueError) as err:
        raw_token_from_request(RequestFactory().get('/'))
    assert err.value.args[0] == 'Missing token.'


def test_plugin_discovery():
    assert json.dumps(toolcall_plugin, indent=4, sort_keys=True)
