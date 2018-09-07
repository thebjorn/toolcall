# -*- coding: utf-8 -*-
from toolcall import jsondecoder
from dkjs import jason


def test_jsondecoder():
    val = dict(
        hello='world',
        dt='2014-06-28T19:51:00+0200',
        ival=42
    )
    assert jsondecoder.loads(jason.dumps(val))
