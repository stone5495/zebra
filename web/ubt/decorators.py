# -*- coding: utf-8 -*-

from functools import wraps

def hello(func):
    @wraps(func)
    def wrapper():
        print "hello world"
        func()
        print "bye world"

    return wrapper
