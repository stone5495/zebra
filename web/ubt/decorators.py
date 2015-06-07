# -*- coding: utf-8 -*-
import redis
from functools import wraps

def hello(func):
    @wraps(func)
    def wrapper():
        print "hello world"
        func()
        print "bye world"

    return wrapper

def cache_to_redis(key):
    print "key {} updated".format(key)
    r_server = redis.Redis('localhost')

    def real_decorator(func):
        @wraps(func)
        def wrapper(*argv, **kwgs):
            print "hell world" + func.__name__
            func(*argv, **kwgs)
            try:
                r_server.incr(key)
            except Exception:
                r_server.set(key, 1)
            finally:
                print "key"
        return wrapper
    return real_decorator
