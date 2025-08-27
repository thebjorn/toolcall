.. message-data:

message-data
-------------
Message data should look similar to::

    {'data': {'exam': u'my-tool',
            'exam_kind': 'start',
            'extra_time': False,
            'firstName': u'User',
            'lastName': u'User',
            'persnr': 'N59928302355241427583868506337734',
            'system': '2:62EQkLe1PB73ouMNVp45iy5v7lI'},
    'msgid': 'b81d465e-c0b5-11e8-9b17-d89ef334a9f2',
    'timestamp': '2018-09-25T13:25:34.534000',
    'token': '1W6obLiMsgHHaIlUHh8h5_GLIynYq2pZLi7Usfn30gwpUObqUX1fxOD092',
    'type': 'person'}

Where 'data' is the payload  and the other top level keys are the envelope.
'msgid' is required to be unique (uuid works well).

You can use the Message class in
https://github.com/thebjorn/toolcall/blob/master/toolcall/message.py
to construct messages, although I do it manually in the sample tool
implementation (https://github.com/thebjorn/toolcall/blob/master/toolcall/toolimplementor/).
