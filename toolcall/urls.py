# -*- coding: utf-8 -*-

""":mod:`toolcall` urls.
"""

from django.conf.urls import *  # pylint:disable=W0401
from . import views


urlpatterns = [

    url(r'^.api/toolcall/v2/$', views.api_definition),
    # url(r'^assessment-begin/$', views.assessment_begin),
    # url(r'^result/$', views.receive_result),
    # url(r'^fetch-token/$', views.fetch_token),      # person

    # debug view
    url(r'^create-token/$', views.create_token),  # start-assessment

]
