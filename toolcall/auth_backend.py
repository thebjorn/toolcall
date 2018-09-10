# -*- coding: utf-8 -*-
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class DKSSOBlindTrustAuthenticator(ModelBackend):
    def authenticate(self, username=None, password=None, **kw):
        if not kw.get('sso_login'):
            return None
        return User.objects.get(username=username)
