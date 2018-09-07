# -*- coding: utf-8 -*-
from dk.collections import pset
import re
import json
from dkjs import jason
from dateutil import parser


class ISO8601Decoder(json.JSONDecoder):
    MAYBE_DATE = re.compile(r'\d\d\d\d-\d\d-\d\d')

    def __init__(self, encoding=None, object_hook=None, parse_float=None,
                 parse_int=None, parse_constant=None, strict=True,
                 object_pairs_hook=None):
        super(ISO8601Decoder, self).__init__(
            encoding,
            object_hook,
            parse_float,
            parse_int,
            parse_constant,
            strict,
            object_pairs_hook or self.objhook)

    def convert(self, val):
        """Convert a single value.
        """
        if not isinstance(val, basestring):
            # if it's not a string, then it has already been converted.
            return val

        if len(val) < 35 and ISO8601Decoder.MAYBE_DATE.match(val) is not None:
            try:
                # XXX: MySQL backend does not support timezone-aware datetimes when USE_TZ is False.
                return parser.parse(val).replace(tzinfo=None)
            except ValueError:
                pass
            try:
                return parser.parse(val)
            except ValueError:
                pass

        return val

    def objhook(self, attrs):
        #return {k: self.convert(v) for k, v in attrs}
        return pset((k, self.convert(v)) for k, v in attrs)


def loads(txt):
    return jason.loads(txt, cls=ISO8601Decoder)
