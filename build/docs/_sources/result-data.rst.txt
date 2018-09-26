
.. _result-data:

result-data
------------
The views in
https://github.com/thebjorn/toolcall/blob/master/toolcall/toolimplementor/views.py 
are what you need to implement/integrate with your code,
:fn:`toolcall.toolimplementor.views.run_my_tool`
creates the result data structure
(and stores it in redis); and
:fn:`toolcall.toolimplementor.views.send_result_data`
returns the result data structure to NorskTest.

The result data should contain the following fields

..
        persnr = models.CharField(…)
        toolcall_participant_id = models.CharField(max_length=150, blank=True, null=True)
        exam = models.CharField(max_length=55)
        score = models.PositiveSmallIntegerField(blank=True, null=True)
        passed = models.BooleanField(default=False)
        tstamp = models.DateTimeField(blank=True, null=True)
        system = models.CharField(max_length=3, null=True)
        exam_kind = models.CharField(max_length=20, null=True)

:persnr:
    the value you received for this field in the start-data.
:toolcall_participant_id:
    an opaque reference to the progress/result data in your system
    (so we can send this to you when resolving issues).
:exam:
    the value you received in start-data [#f1]_
:score:
    integer value reresenting the score the user obtained (optional)
:passed:
    true if the user passed the exam, otherwise false
:tstamp:
    an iso formatted timestamp rerpresnting when the user finished the exam
:system:
    the value you received in start-data
:exam_kind:
    the exam context (optional, e.g. self-test, proctored, etc.),
    should generally be the same as received in start-data.

.. [#f1] extended with adaptive values if needed (e.g. if you’re sent
        "excel" and your exam adapts to user answers you could return e.g.
        "excel:expert", "excel:basics" etc.)

.. todo:: exam and exam_kind is in flux.
