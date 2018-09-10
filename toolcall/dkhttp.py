# -*- coding: utf-8 -*-
"""
    Naming the HTTP response codes.
"""
from django import http


class HttpAccepted(http.HttpResponse):
    status_code = 202


class HttpNoContent(http.HttpResponse):
    status_code = 204


class HttpMultipleChoices(http.HttpResponse):
    status_code = 300


class HttpSeeOther(http.HttpResponse):
    status_code = 303


class HttpNotModified(http.HttpResponse):
    status_code = 304


class HttpBadRequest(http.HttpResponse):
    status_code = 400


class HttpUnauthorized(http.HttpResponse):
    status_code = 401


class HttpForbidden(http.HttpResponse):
    status_code = 403


class HttpNotFound(http.HttpResponse):
    status_code = 404


class HttpMethodNotAllowed(http.HttpResponse):
    status_code = 405


class HttpConflict(http.HttpResponse):
    status_code = 409


class HttpGone(http.HttpResponse):
    status_code = 410


class HttpUnprocessableEntity(http.HttpResponse):
    status_code = 422


class HttpTooManyRequests(http.HttpResponse):
    status_code = 429


class HttpApplicationError(http.HttpResponse):
    status_code = 500


class HttpNotImplemented(http.HttpResponse):
    status_code = 501


class DkHttpError(Exception):
    """Base exception for dk http.
    """
    pass


class ImmediateHttpResponse(DkHttpError):
    """This exception is used to interrupt the flow of processing to immediately
       return a custom HttpResponse.

       Common uses include::

           * for authentication (like digest/OAuth)
           * for throttling

       (from TastyPie).
    """
    _response = http.HttpResponse("Nothing provided.")

    def __init__(self, response):
        self._response = response

    @property
    def response(self):
        return self._response
