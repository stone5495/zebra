#coding=utf-8

from django.core.management import BaseCommand
from django.conf import settings

import time

from excel.models import Excel
from excel.views import unindex_excel


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        print '开始清理资源单'

        now = time.time()
        for excel in Excel.objects.filter(create_time__lte=now-3600*24, status=1):
            unindex_excel(excel)
            print u'%s 已删除' % excel.name
