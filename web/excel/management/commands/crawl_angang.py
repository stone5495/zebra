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



url = 'http://eb.ansteel.cn/sales-web/tpl/p/productSearch'


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        print '开始下载鞍钢网资源单...'
        driver = webdriver.PhantomJS()

        if not os.path.exists(settings.CRAWL_ROOT):
            os.mkdir(settings.CRAWL_ROOT)
            print '新建目录: %s' % settings.CRAWL_ROOT

        today = datetime.datetime.now().strftime('%Y_%m_%d')
        today_dir = os.path.join(settings.CRAWL_ROOT, today)

        if not os.path.exists(today_dir):
            os.mkdir(today_dir)
            print '新建目录: %s' % today_dir

        gangyin_dir = os.path.join(today_dir, 'angang')
        if not os.path.exists(gangyin_dir):
            os.mkdir(gangyin_dir)
            print '新建目录: %s' % gangyin_dir

        try:
            profile = PhoneUserProfile.objects.get(nickname=u'鞍钢资源单', status=2)
        except PhoneUserProfile.DoesNotExist:
            user = User.objects.create_user('__angang', '__angang')
            profile = PhoneUserProfile.objects.create(
                user=user,
                phone='-',
                qq='-',
                nickname=u'鞍钢资源单',
                status=2
            )
            print '系统用户已生成'

        driver.get(url)
        time.sleep(2)
        q = pq(driver.page_source)
        pages = int(pq(q('.pageInfo').find('span')[-1]).text())
        print '一共%d页' % pages


        all_results={}

        for page in range(1, 100):
            driver.get(url+'?p=%d'%page)
            print '第%d页' % page
            #time.sleep(2)
            q = pq(driver.page_source)
            # import pdb
            # pdb.set_trace()
            for _ in range(0,20):
                _1 = _*2
                _2 = _1+1
                _3 = _*4
                _4 = _3+1
                _5 = _*4+3
                try:
                    product_name = pq(q('.abstract')[_]).find('a').text()
                    shop_sign = pq(pq(q('.desSpan')[_3])).text()
                    spec = pq(pq(q('.desSpan')[_4])).text()
                    weight = pq(pq(q('.weight').find('a'))[_]).text()
                    price = pq(pq(q('.prceListTax'))[_]).text()
                    provider_name = pq(pq(q('.companySpan'))[_1]).text()
                    warehouse_name = pq(pq(q('.companySpan'))[_2]).text()
                    special =  pq(pq(q('.desSpan'))[_5]).text()
                    manufacturer = pq(pq(q('.desWeek'))[_1]).text()
                except (IndexError,Exception):
                    continue

                if provider_name not in all_results:
                    all_results[provider_name] = {}

                if product_name not in all_results[provider_name]:
                    all_results[provider_name][product_name] = []

                res = {}
                res['product_name'] = product_name
                res['shop_sign'] = shop_sign
                res['spec'] = spec
                res['weight'] = weight
                res['price'] = price
                res['provider_name'] = provider_name
                res['warehouse_name'] = warehouse_name
                res['special'] = special
                res['manufacturer'] = manufacturer
                all_results[provider_name][product_name].append(res)



        for provider_name, data in all_results.iteritems():
            file_name = u'%s-鞍钢资源单-%s.xls'%(provider_name, today)
            file_path = os.path.join(gangyin_dir, file_name)

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

                for row in rows:
                    c += 1
                    ws.write(c, 0, row['product_name'])
                    ws.write(c, 1, row['shop_sign'])
                    ws.write(c, 2, row['spec'])
                    ws.write(c, 3, row['manufacturer'])
                    ws.write(c, 4, row['warehouse_name'])
                    ws.write(c, 5, row['weight'])
                    ws.write(c, 6, row['price'])
                    ws.write(c, 7, row['special'])

            wb.save(file_path)
            print provider_name, file_path