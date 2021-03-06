# -*- coding: utf-8 -*-

""":mod:`toolcall.tooluser` urls.
"""

from django.conf.urls import *  # pylint:disable=W0401
from . import views

urlpatterns = [
    url(r'^tools/(?P<slug>[-\w\d]+)/$', views.start_tool_redirect),
    url(r'^tools/$', views.list_tools),


    url(r'^start-tool/(?P<slug>[-\w\d]+)/$', views.start_tool),
]
