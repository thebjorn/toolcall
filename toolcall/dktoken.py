# -*- coding: utf-8 -*-

"""Token management.
"""
import struct
import math
import datetime
from base64 import urlsafe_b64encode, urlsafe_b64decode
import os
import time
import zlib
from dk import fstr
from dk.collections import pset


class Token(object):
    """A mostly random token, but with enough structure to validate its
       structure and timeliness.
    """

    class Invalid(ValueError):
        """Exception thrown when token is invalid.
           Call `str(exc)` to get the details.
        """

    @staticmethod
    def inspect(token, now=None):
        if now is None:
            now = time.time()
        elif isinstance(now, datetime.datetime):
            now = time.mktime(now.timetuple())

        def checked():
            return pset(value=None, ok=None)

        def checksum(data, value):
            res = pset()
            res.value = int(value)
            res.data = data
            res.crc32 = zlib.crc32(data)
            res.correct = res.crc32 % 10
            res.ok = res.correct == res.value
            return res

        props = pset((n, None) for n in reversed("""token parts
            length empty padding packet checkdigit2 base64pad
            raw64data data_bytes checkdigit1 rand_length timestamp
            random_bytes valid""".split()))
        props.timestamp = checked()

        try:
            props.token = token
            props.length = len(token)
            props.empty = not token
            t = token.lstrip('=')
            pad = len(token) - len(t)
            props.parts = repr(fstr.fstr(token).split(pad, pad + 1, -2, -1))
            props.padding = pad
            props.packet, ck2 = t[:-1], t[-1]
            props.checkdigit2 = checksum(props.packet, ck2)
            props.base64pad = int(props.packet[0])
            props.raw64data = props.packet[1:-1] + '=' * props.base64pad
            props.data_bytes = urlsafe_b64decode(props.raw64data)
            ck1 = int(props.packet[-1])
            props.checkdigit1 = checksum(props.data_bytes, ck1)
            props.rand_length = len(props.data_bytes) - 4
            msg = struct.unpack('>i%ds' % props.rand_length, props.data_bytes)
            props.timestamp.value = msg[0]
            props.timestamp.now = int(now)
            props.timestamp.ok = msg[0] <= props.timestamp.now
            props.random_bytes = msg[1]
            props.valid = Token(token).valid
        except:
            props.valid = False
            props.pprint()
            raise
        return props

    def __init__(self, incoming=None, length=58):
        self.token = None
        if incoming is None:
            self.token = self.create_new_token(length)
        else:
            self.token = self.validate(incoming)

    def __repr__(self):
        return 'Token(%s)' % self.token

    def __str__(self):
        return self.token

    def __len__(self):
        return len(self.token)

    def __hash__(self):
        return hash(self.token)

    def __eq__(self, other):
        return self.token == other.token


    @property
    def valid(self):
        """Property returning `True` or `False` after calling `validate()`.
        """
        try:
            self.validate(self.token)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate(token):
        """Validate incoming token.

           Raises `Token.Invalid` with the following possible reasons:

           =========================== ========================================
           Token value                 Description
           =========================== ========================================
           token-empty                 Token was an empty string.
           token-syntax-error          Token too short, or has incorrect format.
           token-crc-fail              The checksum was incorrect.
           token-time-syntax-error     Could not parse the timestamp.
           token-premature             The token has a timestamp in the future.
           =========================== ========================================

        """
        if not token:
            raise Token.Invalid('token-empty')

        token = token.lstrip('=')   # remove padding
        try:
            checkdigit2 = token[-1]
            packet = token[:-1]
        except:
            raise Token.Invalid('token-syntax-error')

        if str(zlib.crc32(packet) % 10) != checkdigit2:
            raise Token.Invalid('token-crc2-fail')

        try:
            padlen = int(packet[0])
            rawb64data = packet[1:-1]
            checkdigit1 = int(packet[-1])
        except:
            raise Token.Invalid("wrong-packet-envelope")

        rawb64data += '=' * padlen

        try:
            data_bytes = urlsafe_b64decode(rawb64data)
        except:
            raise Token.Invalid('token-syntax-error')

        if zlib.crc32(data_bytes) % 10 != checkdigit1:
            raise Token.Invalid('token-crc1-fail')

        try:
            rand_length = len(data_bytes) - 4
            timestamp, _random_bytes = struct.unpack('>i%ds' % rand_length,
                                                     data_bytes)
        except:
            raise Token.Invalid('token-unpack-error')

        if timestamp > time.time():
            raise Token.Invalid('token-premature')

        return token

    def create_new_token(self, length=58):
        """Create a new token.

           A token has the following format::

              [pad?][b64-pad-count]b64([random-bytes][timestamp])[cksum1][ck2]

           The `random-bytes` are coming from a cryptographic source, the
           timestamp is the last six digits of `time.time()` (i.e. about
           27 hours), and the checksum is the last digit of a crc32 checksum.
           This is just enough to do some very rudimentary checking.

           The `random-bytes` and `timestamp` are concatenated and encoded
           as (urlsafe) base64, then (an ascii version of) the checksum digit
           is added to the end.
        """
        rand_length = (3 * (length - (8 + 1.0 / 3.0))) / 4.0
        if rand_length < 0:
            raise ValueError("Token length must be >= 10.")
        rand_length = int(math.floor(rand_length))
        random_bytes = os.urandom(rand_length)
        timestamp = int(time.time())
        data_bytes = struct.pack('>i%ds' % rand_length, timestamp, random_bytes)
        checkdigit1 = zlib.crc32(data_bytes) % 10
        b64data = urlsafe_b64encode(data_bytes)
        rawb64data = b64data.rstrip('=')
        padlen = len(b64data) - len(rawb64data)   # 0, 1, or 2
        packet = str(padlen) + rawb64data + str(checkdigit1)
        checkdigit2 = zlib.crc32(packet) % 10
        res = packet + str(checkdigit2)
        reslen = len(res)
        res = '=' * (length - reslen) + res
        return res
