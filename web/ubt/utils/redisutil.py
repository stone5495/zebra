# -*- coding: utf-8 -*-

import redis

class RedisUtil:

    def __init__(self):
        self.r = redis.StrictRedis(host="localhost", port=8882, db="ubt")

    def get(self, key):
        return self.r.get(key)

    def redis_get_all(self, key_name_values):
        """
        带*的key则逐一获取，无*则直接获取
        """
        self.key_name_values = key_name_values
        start_limit = 0
        if "*" in self.key_name_values:
            new_data = {}
            newkey = self.r.keys(self.key_name_values)
            for i in newkey:
                get_data = self.redis_control("get", "%s" % i, "no")
                new_data.setdefault(i, get_data)
        else:
            new_data = self.redis_control("get", "%s" % self.key_name_values)

        return new_data

