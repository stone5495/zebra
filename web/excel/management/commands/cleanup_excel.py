#coding=utf-8

from django.core.management import BaseCommand
from django.conf import settings

import time
from datetime import datetime

from excel.models import Excel
from excel.views import unindex_excel


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        print '开始清理资源单'

        n = datetime.now()
        now = time.mktime(datetime(year=n.year, month=n.month, day=n.day).timetuple())

        for excel in Excel.objects.filter(create_time__lte=now, status=1):
            unindex_excel(excel)
            print u'%s 已删除' % excel.name
