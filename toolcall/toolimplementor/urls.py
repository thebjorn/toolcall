# -*- coding: utf-8 -*-

""":mod:`toolcall.toolimplementor` urls.
"""

from django.conf.urls import *  # pylint:disable=W0401
from . import views

urlpatterns = [
    # api urls (must match urls set in Client model)
    url(r'^start-token/$', views.receive_start_token),
    url(r'^result-token/$', views.send_result_data),

    # demonstration url
    url(r'^start-exam/my-tool/$', views.run_my_tool),
]
