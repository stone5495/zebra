#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

from models import ValidationCode

import sms
import random
import time


def login(request):
    redirect_to = request.POST.get(
        REDIRECT_FIELD_NAME,
        request.GET.get(REDIRECT_FIELD_NAME, '/'))

    if request.method == 'GET':
        phone = request.GET.get('phone', '')
        return render(request, 'login.html', {
            'phone': phone,
            'redirect_to': redirect_to
        })

    phone = request.POST['phone']
    validation_code = request.POST['validation_code']

    user = authenticate(phone=phone, validation_code=validation_code)
    if not user:
        return render(request, 'login.html', {
            'phone': phone,
            'error': u'验证码错误',
            'redirect_to': redirect_to
        })

    auth_login(request, user)
    return HttpResponseRedirect(redirect_to)


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')


def send_validation_code(request):
    phone = request.GET.get('phone')
    now = time.time()

    if ValidationCode.objects.filter(phone=phone, status=1, create_time__gte=now-90).exists():
        return HttpResponse(u'发送过于频繁', status=403)

    ValidationCode.objects.filter(phone=phone).update(status=0)
    validation_code = str(random.randint(1000, 9999))
    ValidationCode.objects.create(
        phone=phone, 
        code=validation_code, 
        status=1,
        create_time=now,
        expire_time=now+600)

    sms.send_validation_code(phone, validation_code)
    return HttpResponse(validation_code)


@login_required
def profile(request):
    profile = request.user.phoneuserprofile

    if request.method == 'POST':
        profile.nickname = request.POST.get('nickname', '')
        profile.qq = request.POST.get('qq', '')
        profile.save()

    context = {
        'phone': profile.phone,
        'nickname': profile.nickname,
        'qq': profile.qq
    }
    return render(request, 'profile.html', context)



