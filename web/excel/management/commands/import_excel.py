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
        print '开始导入找钢网资源单...'

        try:
            profile = PhoneUserProfile.objects.get(nickname=u'找钢网资源单', status=2)
        except PhoneUserProfile.DoesNotExist:
            user = User.objects.create_user('__zhaogang', '__zhaogang')
            profile = PhoneUserProfile.objects.create(
                user=user,
                phone='-',
                qq='-',
                nickname=u'找钢网资源单',
                status=2
            )
            print '系统用户已生成'

        crawl_excels = CrawlExcel.objects.filter(source=1, imported=False)

        for crawl_excel in crawl_excels:
            excel = Excel.objects.create(
                create_time = time.time(),
                user = profile.user,
                name = os.path.basename(crawl_excel.filepath),
                status = 0,
                excel_file = File(file(crawl_excel.filepath))
            )
            try:
                index_excel(excel)
                print 'indexed %s'%excel.name
            except:
                print 'wrong %s'%excel.name

            crawl_excel.imported = True
            crawl_excel.save()


