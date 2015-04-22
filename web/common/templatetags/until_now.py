#coding=utf-8
from django import template

import time

register = template.Library()

@register.filter
def until_now(value):
    v = int(time.time() - value)

    if v < 60:
        return u'1分钟内'

    if v < 60*60:
        return u'%d分钟前'%(v/60)

    if v < 60*60*24:
        return u'%d小时前'%(v/60/60)

    return u'一天前'