# -*- coding: utf-8 -*-

from toolcall import defaults


def test_defaults():
    assert defaults.TOOLCALL_TOKEN_TIMEOUT_SECS == 1
    assert defaults.TOOLCALL_TOKEN_SIZE == 51
