#coding=utf-8
from django.db import models
from django.contrib.auth.models import User


class ValidationCode(models.Model):
    create_time = models.FloatField()
    expire_time = models.FloatField()

    code = models.CharField(max_length=4)
    phone = models.CharField(max_length=11)
    status = models.IntegerField()


class PhoneUserProfile(models.Model):

    user = models.OneToOneField(User)
    phone = models.CharField(max_length=11)
    
    qq = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20)

    status = models.IntegerField()