#coding=utf-8

from django.core.management import BaseCommand
from django.conf import settings

from selenium import webdriver
from pyquery.pyquery import PyQuery as pq

import os, datetime, time
import requests, urllib, redis

from excel.models import CrawlExcel
from account.models import PhoneUserProfile
from django.contrib.auth.models import User

import json, math, xlwt


url = 'http://www.shgt.com/query/general_packs_search/'


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        print '开始下载上海钢铁交易中心资源单...'

        if not os.path.exists(settings.CRAWL_ROOT):
            os.mkdir(settings.CRAWL_ROOT)
            print '新建目录: %s' % settings.CRAWL_ROOT

        today = datetime.datetime.now().strftime('%Y_%m_%d')
        today_dir = os.path.join(settings.CRAWL_ROOT, today)

        if not os.path.exists(today_dir):
            os.mkdir(today_dir)
            print '新建目录: %s' % today_dir

        zhaogang_dir = os.path.join(today_dir, 'shgt')
        if not os.path.exists(zhaogang_dir):
            os.mkdir(zhaogang_dir)
            print '新建目录: %s' % zhaogang_dir

        try:
            profile = PhoneUserProfile.objects.get(nickname=u'上海钢铁交易中心资源单', status=2)
        except PhoneUserProfile.DoesNotExist:
            user = User.objects.create_user('__shgt', '__shgt')
            profile = PhoneUserProfile.objects.create(
                user=user,
                phone='61381166-6',
                qq='-',
                nickname=u'上海钢铁交易中心资源单',
                status=2
            )
            print '系统用户已生成'

        post_body = {
            "search":"group=0__local_site=1__out_site=0",
            "shop":"",
            "query":"",
            "mode":"package_list",
            "page":1,
            "page_size":100,
            "sort":""
        }

        r = requests.post(url, json=post_body)
        b = json.loads(r.text)['meta'][0][1]

        pages = int(math.ceil(b/100.0))
        print '一共%d页' % pages

        all_results = {}

        for page in range(1, pages+1):
            print '第%d页' % page
            time.sleep(1)
            post_body['page'] = page

            r = requests.post(url, json=post_body)
            records = json.loads(r.text)['result']

            for record in records:
                provider_name = record['provider_name']
                if provider_name not in all_results:
                    all_results[provider_name] = {}

                product_name = record['product_name']
                if product_name not in all_results[provider_name]:
                    all_results[provider_name][product_name] = []

                all_results[provider_name][product_name].append(record)


        for provider_name, data in all_results.iteritems():
            file_name = u'%s-上海钢铁交易中心-%s.xls'%(provider_name, today)
            file_path = os.path.join(zhaogang_dir, file_name)

            wb = xlwt.Workbook()
            for product_name, rows in data.iteritems():
                ws = wb.add_sheet(product_name)
                c = 0
                ws.write(c, 0, u'品名')
                ws.write(c, 1, u'牌号')
                ws.write(c, 2, u'规格')
                ws.write(c, 3, u'产地')
                ws.write(c, 4, u'仓库')
                ws.write(c, 5, u'重量')
                ws.write(c, 6, u'价格')
                ws.write(c, 7, u'说明1')
                ws.write(c, 8, u'说明2')
                ws.write(c, 9, u'说明3')

                for row in rows:
                    c += 1
                    ws.write(c, 0, row['product_name'])
                    ws.write(c, 1, row['shop_sign'])
                    ws.write(c, 2, row['spec'])
                    ws.write(c, 3, row['manufacturer'])
                    ws.write(c, 4, row['warehouse_name'])
                    ws.write(c, 5, row['weight'])
                    ws.write(c, 6, row['discounted_price'])
                    ws.write(c, 7, row['special'])
                    ws.write(c, 8, row['pack_comments'])
                    ws.write(c, 9, row['pack_comments2'])

            wb.save(file_path)
            print provider_name, file_path


        #     q = pq(driver.page_source)
        #     q = q('table tr')

        #     for _ in q[1:]:
        #         excel_id = pq(pq(_).find('a')[-2]).attr('vals')

        #         if CrawlExcel.objects.filter(source=1, source_id=excel_id).exists():
        #             continue

        #         try:
        #             r = requests.get(download_url % excel_id, stream=True)
        #             file_name = urllib.unquote(r.headers['content-disposition'].split('=')[1])

        #             print '下载中: [%s] %s' % (excel_id, file_name)
        #             file_path = os.path.join(zhaogang_dir, file_name)

        #             f = open(file_path, 'wb')
        #             for block in r.iter_content(1024):
        #                 if not block:
        #                     break
        #                 f.write(block)
        #             f.close()

        #             CrawlExcel.objects.create(
        #                 create_time=time.time(),
        #                 crawl_user=profile.user,
        #                 source=1,
        #                 source_id=excel_id,
        #                 filepath=file_path,
        #                 imported=False
        #             )

        #         except Exception as e:
        #             print '错误: [%s]' % excel_id
        #             import traceback
        #             traceback.print_exc()

        # driver.close()
