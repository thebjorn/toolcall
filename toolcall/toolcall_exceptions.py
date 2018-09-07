# -*- coding: utf-8 -*-

"""Toolcall exception hierarchy.
"""


class ToolcallException(Exception):
    """Toolcall exception base class.
    """


class ToolcallInvalidResponse(ToolcallException):
    """Something other than a 200 OK response.
    """


class ToolcallJSonDecodeError(ToolcallException):
    """Couldn't decode json value.
    """


class ToolcallMessageException(ToolcallException):
    """Generic message error.
    """


class ToolcallResultException(ToolcallMessageException):
    """Something is wrong with the result.
    """
