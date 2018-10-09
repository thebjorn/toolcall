# -*- coding: utf-8 -*-
import datetime

from django import shortcuts as dj, template
from django.contrib.auth.decorators import login_required
from dkredis import dkredis

import toolcall.message
from toolcall import defaults
from toolcall.dktoken import Token
from toolcall.models import Tool, ToolCall


# def encrypt_user(usr):
#     from cryptography.fernet import Fernet
#     key = Fernet.generate_key()
#     f = Fernet(key)
#     return f.encrypt(str(usr.id))


def generate_unique_id(usr):
    p = 59928302355241427583868506337732
    return 'N' + str(p ^ usr.id)


def fetch_progress_record(user, tool):
    ToolCall.close_open_attempts(tool, user)
    now = datetime.datetime.now()
    progress = None

    # if tool.restartable:
    #     restart_cutoff = now - datetime.timedelta(
    #         minutes=tool.restart_duration_minutes)
    #     open_attempts = list(ToolCall.objects.filter(
    #         tool=tool,
    #         user=user,
    #         ended__isnull=True,
    #         started__gt=restart_cutoff
    #     ).order_by('-started'))
    #     if open_attempts:
    #         kind = 'restart'
    #         progress = open_attempts[0]
    #         for tcall in open_attempts[1:]:
    #             tcall.timed_out(now)
    if not progress:
        progress = ToolCall.objects.create(
            tool=tool,
            user=user,
            started=now,
            status='initial'
        )
    return progress


# finlib.__quizz:begin__assessment
@login_required
def start_tool(request, slug):
    """User clicked on start-tool button.
    """
    tool = dj.get_object_or_404(Tool, slug=slug)
    progress = fetch_progress_record(request.user, tool)

    token = Token()

    url = tool.client.receive_start_token_url
    url += '?access_token=%s' % token

    usr = request.user
    value = toolcall.message.Message(
        "person", token,
        firstName=usr.first_name,
        lastName=usr.last_name,
        email=usr.email,
        exam=tool.slug,
        persnr=generate_unique_id(usr),
        extra_time=False,  # usr.has_perm(...)
        exam_kind='start',

        system=progress.sign()
    )

    dkredis.set_pyval('TOKEN-%s' % token,
                      value,
                      defaults.TOOLCALL_TOKEN_TIMEOUT_SECS)

    progress.set_status('start-tk-sent')
    return dj.render_to_response(
        'toolcall/tooluser/start-tool.html',
        template.Context({
            "tool": tool,
            "token": Token(),
            "value": value,
            "url": url,
            "progress": progress,
            "request": request
        })
    )
