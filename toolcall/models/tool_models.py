# -*- coding: utf-8 -*-
import datetime

from django.contrib.contenttypes.models import ContentType
from django.core.signing import Signer
from django.db import models
from django.contrib.auth.models import User, Permission


# from dkexam.models import Result, Assessment
from toolcall.models import legal_transitions


class Client(models.Model):
    """An API client.
    """
    name = models.CharField(max_length=100, unique=True)

    client_secret = models.CharField(
        max_length=255,  # 32
        help_text="We sign transmissions using this as key to "
                  "``django.core.signing.Signer``.")

    receive_start_token_url = models.CharField(
        max_length=255,
        help_text="Url where we redirect the end user with a token.")
    receive_start_data_url = models.CharField(
        max_length=255,
        help_text="Url where we send start data for user.")
    receive_result_token_url = models.CharField(
        max_length=255,
        help_text="Url where we return the result token and expect result "
                  "data in return")

    class Meta:
        permissions = [
            ("client_admin", "Can administrate toolcall client(s).")
        ]

    @classmethod
    def make_client_admin(cls, usr):
        content_type = ContentType.objects.get_for_model(Client)
        permission = Permission.objects.get(content_type=content_type,
                                            codename='client_admin')
        usr.user_permissions.add(permission)


class Tool(models.Model):
    """Available tools.
    """
    #: the client the tool belongs to
    client = models.ForeignKey(Client)
    slug = models.SlugField(
        unique=True,
        help_text=u"This is the 'id' we send to the tool provider to start"
                  u"this tool.")
    name = models.CharField(
        max_length=100,
        help_text=u"The end-user visible name of the tool.")
    description = models.CharField(
        max_length=255, null=True, blank=True,
        help_text=u"A short, end-user visible, description of the tool.")
    icon = models.URLField(
        null=True, blank=True,
        help_text=u"The uri of an end-user visible icon representing the Tool.")

    restartable = models.BooleanField(default=False)
    restart_duration_minutes = models.PositiveIntegerField(
      null=True, blank=True)

    def __unicode__(self):
        return self.name


class ToolCall(models.Model):
    tool = models.ForeignKey(Tool)
    user = models.ForeignKey(User)
    started = models.DateTimeField(null=True, blank=True)
    ended = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=legal_transitions.choices,
        default='initial'
    )

    def __unicode__(self):
        return "{self.tool.name} {self.user.username} {self.started} {self.status}".format(
            self=self
        )

    def save(self, *args, **kwargs):
        super(ToolCall, self).save(*args, **kwargs)
        self.logs.create(status=self.status)

    @classmethod
    def close_open_attempts(cls, tool, user):
        open_attempts = cls.objects.filter(
            tool=tool, user=user, ended__isnull=True
        )
        for attempt in open_attempts:
            attempt.close()

    def sign(self):
        signer = Signer()
        return signer.sign(str(self.id))

    @classmethod
    def get(cls, signature):
        signer = Signer()
        return cls.objects.get(id=signer.unsign(signature))

    def set_status(self, status):
        if status not in legal_transitions.transitions[self.status]:
            print """
                OOPS..: %s -> %s is not a legal transition
                (legal transitions: %r)
            """ % (self.status, status,
                   legal_transitions.transitions[self.status])
        self.status = status
        self.save()

    def timed_out(self, when=None):
        if when is None:
            when = datetime.datetime.now()
        self.ended = when
        self.set_status('tool-timeout-err')

    def close(self):
        self.ended = datetime.datetime.now()
        self.set_status('finished-err')

    def finished_ok(self):
        self.ended = datetime.datetime.now()
        self.set_status('finished-ok')


class ToolCallLog(models.Model):
    toolcall = models.ForeignKey(ToolCall, related_name='logs')
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=18)
    details = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return "%s : %s" % (self.timestamp, self.status)

    class Meta:
        ordering = ['timestamp']


class ToolcallResult(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    toolcall_participant_id = models.CharField(
        max_length=150, blank=True, null=True)
    exam = models.CharField(max_length=55)
    score = models.PositiveSmallIntegerField(blank=True, null=True)
    passed = models.BooleanField(default=False)
    tstamp = models.DateTimeField(auto_now_add=True)
    toolcall_tstamp = models.DateTimeField(blank=True, null=True)
    system = models.CharField(max_length=3, null=True)
    exam_type = models.CharField(max_length=20, null=True)

    def __unicode__(self):
        return self.toolcall_participant_id

    def __repr__(self):
        return '<ToolcallResult %r>' % self.__dict__

    @property
    def kind(self):
        """Is this a quiz or an exam?
        """
        if self.exam in conf.TOOLCALL_QUIZZES:
            return 'quiz'
        if self.exam in conf.TOOLCALL_EXAMS:
            return 'exam'
        return 'unknown'

    def result(self):
        """Create a dkexam.models.Result object for this toolcall result.

           This will run signals, rules, etc.
        """
        if self.system in {'fin', 'finaut'}:
            self.system = 'afr'
        assessment_key = "%s-%s" % (self.exam, self.system)
        assmt_id = conf.DKEXAM_ASSESSMENT_ID[assessment_key]

        result, res_exist = Result.objects.get_or_create(
            assessment_id=assmt_id,
            external_resultid='toolcall:%s' % self.toolcall_participant_id
        )
        # any attributes that can be changed post-hoc should not be part
        # of get_or_create.
        result.user = self.user
        result.datetime_finished = self.tstamp
        result.passing_grade = self.passed
        result.percentage_score = self.score
        if not res_exist:
            result.attempt_number = result.find_attempt_number()
        result.save()
        return result

    def save(self, *args, **kwargs):
        super(ToolcallResult, self).save(*args, **kwargs)
        self.result()

    @classmethod
    def store(cls, result):
        if result.type != 'result':
            raise ValueError(
                "Incorrect type: %r expected 'result'" % result.type
            )

        res, _ = cls.objects.get_or_create(
            user=User.objects.get(persnr=result.data.persnr),
            # persnr=UserPersnr.fetch(result.data.persnr),
            toolcall_participant_id=result.data.participation_id,
            passed=result.data.passed,
            exam=result.data.exam,
            score=result.data.score,
            toolcall_tstamp=result.timestamp,
            system=result.data.system,
            exam_type=result.data.exam_type
            # token=result.token
        )
        return res
