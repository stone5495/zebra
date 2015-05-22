#coding=utf-8
from django.contrib.auth.models import User
from models import ValidationCode, PhoneUserProfile

import time


class SmsBackend(object):

    def authenticate(self, phone=None, validation_code=None):
        now = time.time()

        code_query = ValidationCode.objects.filter(phone=phone, status=1, expire_time__gte=now)

        if not code_query.exists():
            return None

        if code_query.count() != 1:
            return None

        if code_query[0].code != validation_code:
            return None

        current_code = code_query[0]
        current_code.status = 0
        current_code.save()

        username = 'phone_%s'%phone
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create_user(username, password=phone)
            phone_user = PhoneUserProfile.objects.create(
                user=user, 
                phone=phone, qq='', nickname='', status=1)

        return user


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

