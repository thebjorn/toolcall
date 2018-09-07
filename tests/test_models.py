# -*- coding: utf-8 -*-
from toolcall.models import ToolcallResult


def test_model_toolcallresult():
    hr = ToolcallResult.objects.get(pk=118121)
    assert unicode(hr) == hr.toolcall_participant_id

    assert repr(hr).startswith('<ToolcallResult')

    # assert hr.kind == 'charting'

    assert hr.user.id == hr.user().id

    r = hr.result()
    assert not r.passing_grade
