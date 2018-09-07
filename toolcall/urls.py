# -*- coding: utf-8 -*-

""":mod:`toolcall` urls.
"""

from django.conf.urls import *  # pylint:disable=W0401

urlpatterns = patterns(
    'toolcall',

    # (r'^$', 'views.plugin_definition'),
    (r'^assessment-begin/$', 'views.assessment_begin'),
    (r'^result/$', 'views.receive_result'),
    (r'^fetch-token/$', 'views.fetch_token'),      # person

    # debug view
    (r'^create-token/$', 'views.create_token'),  # start-assessment

)
