# -*- coding: utf-8 -*-
from toolcall.message import Message
from dkjs import jason
from toolcall.toolcallexceptions import ToolcallException, ToolcallJSonDecodeError, ToolcallResultException, ToolcallMessageException
import pytest
from toolcall.toolcallresult import fetch_result_token


class MockGetter(object):
    ok = True

    def __init__(self, val):
        self.text = jason.dumps(val)

    def __call__(self, *args, **kw):
        return self


def test_fetch_result_token():
    with pytest.raises(ToolcallJSonDecodeError):
        fetch_result_token('token', MockGetter(""))

    with pytest.raises(ToolcallResultException) as err:
        fetch_result_token('xxx', MockGetter(dict(hello='world')))
    assert err.value.args[0].startswith("Missing token in result:")

    with pytest.raises(ToolcallResultException) as err:
        fetch_result_token('xxx', MockGetter(dict(token='hello')))
    assert err.value.args[0].startswith("Result has unexpected token")

    with pytest.raises(ToolcallMessageException) as err:
        fetch_result_token('xxx', MockGetter(Message('result', 'xxx', hello='world')))
    assert err.value.args[0].startswith("Message missing 'persnr'")

    res = fetch_result_token('xxx',
                             MockGetter(Message(
                                 'result', 'xxx',
                                 persnr='12345678901',
                                 participant_id='part-id',
                                 passed=False,
                                 exam='samtalen',
                                 score=50,
                                 system='afr',
                                 exam_type='exam'
                             )))
    assert res.data.persnr == '12345678901'
