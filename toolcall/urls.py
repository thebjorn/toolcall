# -*- coding: utf-8 -*-

""":mod:`toolcall` urls.
"""

from django.conf.urls import *  # pylint:disable=W0401
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += [
    # tool user
    url(r'^tooluser/', include('toolcall.tooluser.urls')),

    # tool implementor (client)
    url(r'^client/', include('toolcall.toolimplementor.urls')),

    # server api
    url(r'^.api/toolcall/v2/$', views.api_definition),
    url(r'^fetch-token/$', views.fetch_token),      # person

    # url(r'^assessment-begin/$', views.assessment_begin),
    url(r'^result/$', views.receive_result),

    # debug view
    url(r'^create-token/$', views.create_token),  # start-assessment

]
