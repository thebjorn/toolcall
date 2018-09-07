# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User, Permission


# from dkexam.models import Result, Assessment


class Client(models.Model):
    """An API client.
    """
    name = models.CharField(max_length=100)

    client_secret = models.CharField(
        max_length=255,
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


# class ToolcallAssessments(models.Model):
#     assessment_tag = models.CharField(max_length=50)
#     assessment = models.ForeignKey(Assessment)
#
#     active = models.BooleanField(default=True)
#     active_start = models.DateTimeField(auto_now_add=True)
#     active_end = models.DateTimeField(null=True, blank=True)
#
#     def __unicode__(self):
#         return self.assessment_tag


# class ToolcallResult(models.Model):
#     user = models.ForeignKey(User, blank=True, null=True)
#     toolcall_participant_id = models.CharField(max_length=150, blank=True, null=True)
#     exam = models.CharField(max_length=55)
#     score = models.PositiveSmallIntegerField(blank=True, null=True)
#     passed = models.BooleanField(default=False)
#     tstamp = models.DateTimeField(auto_now_add=True)
#     toolcall_tstamp = models.DateTimeField(blank=True, null=True)
#     system = models.CharField(max_length=3, null=True)
#     exam_type = models.CharField(max_length=20, null=True)
#
#     def __unicode__(self):
#         return self.toolcall_participant_id
#
#     def __repr__(self):
#         return '<ToolcallResult %r>' % self.__dict__
#
#     @property
#     def kind(self):
#         """Is this a quiz or an exam?
#         """
#         if self.exam in conf.TOOLCALL_QUIZZES:
#             return 'quiz'
#         if self.exam in conf.TOOLCALL_EXAMS:
#             return 'exam'
#         return 'unknown'
#
#     def result(self):
#         """Create a dkexam.models.Result object for this toolcall result.
#
#            This will run signals, rules, etc.
#         """
#         if self.system in {'fin', 'finaut'}:
#             self.system = 'afr'
#         assessment_key = "%s-%s" % (self.exam, self.system)
#         assmt_id = conf.DKEXAM_ASSESSMENT_ID[assessment_key]
#
#         result, res_exist = Result.objects.get_or_create(
#             assessment_id=assmt_id,
#             external_resultid='toolcall:%s' % self.toolcall_participant_id
#         )
#         # any attributes that can be changed post-hoc should not be part
#         # of get_or_create.
#         result.user = self.user
#         result.datetime_finished = self.tstamp
#         result.passing_grade = self.passed
#         result.percentage_score = self.score
#         if not res_exist:
#             result.attempt_number = result.find_attempt_number()
#         result.save()
#         return result
#
#     def save(self, *args, **kwargs):
#         super(ToolcallResult, self).save(*args, **kwargs)
#         self.result()
#
#     @classmethod
#     def store(cls, result):
#         if result.type != 'result':
#             raise ValueError(
#                 "Incorrect type: %r expected 'result'" % result.type
#             )
#
#         res, _ = cls.objects.get_or_create(
#             user=User.objects.get(persnr=result.data.persnr),
#             # persnr=UserPersnr.fetch(result.data.persnr),
#             toolcall_participant_id=result.data.participation_id,
#             passed=result.data.passed,
#             exam=result.data.exam,
#             score=result.data.score,
#             toolcall_tstamp=result.timestamp,
#             system=result.data.system,
#             exam_type=result.data.exam_type
#             # token=result.token
#         )
#         return res
