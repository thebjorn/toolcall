# -*- coding: utf-8 -*-
from base64 import urlsafe_b64encode
import pytest
from toolcall.dktoken import Token


def test_token():
    t = Token()
    t.validate(t.token)
    assert Token().valid
    assert type(Token().token) == str


def test_roundtrip():
    t = Token()
    u = Token(t.token)
    assert t == u
    assert str(t) == str(u)
    assert repr(t) == repr(u)
    assert hash(t) == hash(u)


def test_invalid():
    with pytest.raises(Token.Invalid) as err:
        Token("")
    assert err.value.args[0] == 'token-empty'

    with pytest.raises(Token.Invalid) as err:
        Token("foo")
    assert err.value.args[0] == 'token-crc2-fail'

    with pytest.raises(Token.Invalid) as err:
        Token(urlsafe_b64encode('hello world') + 'X')
    assert err.value.args[0] == 'token-crc2-fail'

    with pytest.raises(ValueError) as err:
        Token(length=1)


def test_length():
    for i in range(9, 30):
        assert len(Token(length=i)) == i
