#coding=utf-8

from django.core.management import BaseCommand
from django.conf import settings

import os, datetime, time

from account.models import PhoneUserProfile
from excel.models import Excel
from django.contrib.auth.models import User
from django.core.files import File
from excel.views import index_excel

from excel.models import CrawlExcel


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        print '开始导入资源单...'

        crawl_excels = CrawlExcel.objects.filter(imported=False)
        print '%s 个excel需要导入' % crawl_excels.count()

        for crawl_excel in crawl_excels:
            excel = Excel.objects.create(
                create_time = crawl_excel.create_time,
                user = crawl_excel.crawl_user,
                name = os.path.basename(crawl_excel.filepath),
                status = 0,
                excel_file = File(file(crawl_excel.filepath))
            )
            try:
                index_excel(excel)
                print 'indexed %s'%excel.id
            except:
                print 'wrong %s'%excel.id

            crawl_excel.imported = True
            crawl_excel.save()


