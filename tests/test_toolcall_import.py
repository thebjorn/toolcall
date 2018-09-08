# -*- coding: utf-8 -*-

"""Test that all modules are importable.
"""

import toolcall.admin
import toolcall.apps
import toolcall.cls2pset
import toolcall.defaults
import toolcall.dkplugin
import toolcall.dkpluginbase
import toolcall.toolcall_exceptions
import toolcall.toolresult
import toolcall.jsondecoder
import toolcall.models
import toolcall.urls
import toolcall.views


def test_import_():
    "Test that all modules are importable."
    
    assert toolcall.admin
    assert toolcall.apps
    assert toolcall.cls2pset
    assert toolcall.defaults
    assert toolcall.dkplugin
    assert toolcall.dkpluginbase
    assert toolcall.toolcall_exceptions
    assert toolcall.toolresult
    assert toolcall.jsondecoder
    assert toolcall.models.models
    assert toolcall.urls
    assert toolcall.views
