# -*- coding: utf-8 -*-
import datetime
import json

from django.http import HttpResponse

from ..models import HourBehaviour
from ..utils.excelutil import generate_excel
from ..utils.redisutil import RedisUtil

yesterday_date = datetime.date.today() - datetime.timedelta(days=1)

class OverView(object):

    def __init__(self, request):
        """
        :param request: 获取请求中的参数
        :初始化对象，取出今日和昨日的所有小时记录，以备后续数据处理

        """
        self.request = request
        self.hourly_records_today = HourBehaviour.objects.filter(record_date=datetime.date.today().strftime("%Y-%m-%d"))
        self.hourly_records_yes = HourBehaviour.objects.filter(record_date=yesterday_date.strftime("%Y-%m-%d"))

    def get_daily(self):

        today = {"pv": 0, "uv": 0, "ID": 0, "search": 0, "download": 0, "regi": 0}
        yesterday = {"pv": 0, "uv": 0, "ID": 0, "search": 0, "download": 0, "regi": 0}

        for record in self.hourly_records_today:
            today["pv"] += record.page_view
            today["uv"] += record.user_view
            today["ID"] += record.login_cnt
            today["search"] += record.search_cnt
            today["download"] += record.download_cnt
            today["regi"] += record.register_cnt

        for record in self.hourly_records_yes:
            yesterday["pv"] += record.page_view
            yesterday["uv"] += record.user_view
            yesterday["ID"] += record.login_cnt
            yesterday["search"] += record.search_cnt
            yesterday["download"] += record.download_cnt
            yesterday["regi"] += record.register_cnt

        #此处需要根据算法得出
        predict = {}

        result = {"today": today, "yesterday": yesterday, "predict": predict}
        return HttpResponse(json.dumps(result), content_type="application/json")

    def get_overview(self):

        today = {"pv": [], "uv": [], "ID": [], "search": [], "download": [], "regi": [], "key": []}
        yesterday = {"pv": [], "uv": [], "ID": [], "search": [], "download": [], "regi": [], "key": []}

        for record in self.hourly_records_today:
            today["pv"].append(record.page_view)
            today["uv"].append(record.user_view)
            today["ID"].append(record.login_cnt)
            today["search"].append(record.search_cnt)
            today["download"].append(record.download_cnt)
            today["regi"].append(record.register_cnt)
            today["key"].append(record.hour.split("-")[2])

        for record in self.hourly_records_yes:
            yesterday["pv"].append(record.page_view)
            yesterday["uv"].append(record.user_view)
            yesterday["ID"].append(record.login_cnt)
            yesterday["search"].append(record.search_cnt)
            yesterday["download"].append(record.download_cnt)
            yesterday["regi"].append(record.register_cnt)
            yesterday["key"].append(record.hour.split("-")[2])

        keys = yesterday["key"] if len(yesterday["key"]) > len(today["key"]) else today["key"]
        del yesterday["key"]
        del today["key"]

        result = {"today": today, "yesterday": yesterday, "keys": keys}
        return HttpResponse(json.dumps(result), content_type="application/json")

    def get_search(self):
        """
        :return: from redis
        """
        r = RedisUtil()
        all_search = r.redis_get_all("search_*")
        #sort_search = sorted(all_search.items(), key=lambda d: d[1], reverse=True)
        backitems = [[v[1], v[0]] for v in all_search.items()]
        backitems.sort(reverse=True)
        return HttpResponse(json.dumps(backitems[5]), content_type="application/json")

    def get_download(self):

        """
        :return: from redis
        """
        r = RedisUtil()
        all_search = r.redis_get_all("download_*")
        backitems = [[v[1], v[0]] for v in all_search.items()]
        backitems.sort(reverse=True)
        return HttpResponse(json.dumps(backitems[5]), content_type="application/json")

    def get_crawl(self):

        today = {"crawl": [], "key": []}
        yesterday = {"crawl": [], "key": []}

        for record in self.hourly_records_today:
            today["crawl"].append(record.crawl_cnt)
            today["key"].append(record.hour.split("-")[2])

        for record in self.hourly_records_yes:
            yesterday["crawl"].append(record.crawl_cnt)
            yesterday["key"].append(record.hour.split("-")[2])

        keys = yesterday["key"] if len(yesterday["key"]) > len(today["key"]) else today["key"]
        del yesterday["key"]
        del today["key"]

        result = {"today": today, "yesterday": yesterday, "keys": keys}
        return HttpResponse(json.dumps(result), content_type="application/json")

    def get_upload(self):
        today = {"upload": [], "key": []}
        yesterday = {"upload": [], "key": []}

        for record in self.hourly_records_today:
            today["upload"].append(record.page_view)
            today["key"].append(record.hour.split("-")[2])

        for record in self.hourly_records_yes:
            yesterday["upload"].append(record.page_view)
            yesterday["key"].append(record.hour.split("-")[2])

        keys = yesterday["key"] if len(yesterday["key"]) > len(today["key"]) else today["key"]
        del yesterday["key"]
        del today["key"]

        result = {"today": today, "yesterday": yesterday, "keys": keys}
        return HttpResponse(json.dumps(result), content_type="application/json")

    def get_excel(self):
        return generate_excel("overview")
