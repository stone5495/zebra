#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from django.core.management import BaseCommand
from django.conf import settings

from selenium import webdriver
from pyquery.pyquery import PyQuery as pq

import os, datetime, time,re
import requests, urllib, redis

from excel.models import CrawlExcel
from account.models import PhoneUserProfile
from django.contrib.auth.models import User
import json, math, xlwt


url ='http://www.opsteel.cn/resource/shanghai.html'
url2 = 'http://www.opsteel.cn/resource/shanghai'


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        print '开始下载欧普钢网资源单...'
        driver = webdriver.PhantomJS()

        if not os.path.exists(settings.CRAWL_ROOT):
            os.mkdir(settings.CRAWL_ROOT)
            print '新建目录: %s' % settings.CRAWL_ROOT

        today = datetime.datetime.now().strftime('%Y_%m_%d')
        # yesday = datetime.datetime.now() + datetime.timedelta(days=-1)
        # yesday_str = yesday.strftime('%m-%d')
        yesday_str = datetime.datetime.now().strftime('%m-%d')
        zhPattern = re.compile(u'[\u4e00-\u9fa5]+')

        print yesday_str
        today_dir = os.path.join(settings.CRAWL_ROOT, today)

        if not os.path.exists(today_dir):
            os.mkdir(today_dir)
            print '新建目录: %s' % today_dir

        gangyin_dir = os.path.join(today_dir, 'oupu')
        if not os.path.exists(gangyin_dir):
            os.mkdir(gangyin_dir)
            print '新建目录: %s' % gangyin_dir

        try:
            profile = PhoneUserProfile.objects.get(nickname=u'欧普钢网资源单', status=2)
        except PhoneUserProfile.DoesNotExist:
            user = User.objects.create_user('__oupu', '__oupu')
            profile = PhoneUserProfile.objects.create(
                user=user,
                phone='-',
                qq='-',
                nickname=u'欧普钢网资源单',
                status=2
            )
            print '系统用户已生成'

        driver.get(url)
        time.sleep(2)
        q = pq(driver.page_source)
        # pages = int(pq(q('.z-end')).attr('id'))
        pages = 500
        print '一共%d页' % pages

        all_results={}

        for page in range(1, pages+1):
            driver.get(url2+'_%d.html'%page)
            print '第%d页' % page
            time.sleep(2)

            q = pq(driver.page_source)
            q = q('table tr')
            # import pdb
            # pdb.set_trace()
            break_out = False
            for _ in range(1,24):
                try:
                    product_name = pq(pq(q('tr')[_])('td')[1]).text()
                    shop_sign = pq(pq(q('tr')[_])('td')[3]).text()
                    spec = pq(pq(q('tr')[_])('td')[2]).text()
                    weight = pq(pq(pq(q('tr')[_])('td')[6]).find('p')[0]).text()
                    price = pq(pq(q('tr')[_])('td')[5]).text()
                    provider_name = pq(pq(pq(q('tr')[_])('td')[9]).find('a')[0]).text()
                    release_time = pq(pq(q('tr')[_])('td')[8]).text()
                    print yesday_str
                    print release_time
                    print provider_name

                    if provider_name == '':
                        provider_name = '欧浦商城'
                        contacts = '欧浦商城华东站热线'
                        phone = '021-60717078-8'

                    else:
                        match = zhPattern.search(release_time)
                        if match == None:
                            if release_time != yesday_str:

                                break_out = True
                                break
                        contacts = pq(pq(pq(q('tr')[_])('td')[9]).find('em')[0]).text()
                        phone = pq(pq(pq(q('tr')[_])('td')[9]).find('em')[1]).text()
                    warehouse_name = pq(pq(q('tr')[_])('td')[7]).text()
                    manufacturer =  pq(pq(q('tr')[_])('td')[4]).text()

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
                res['manufacturer'] = manufacturer
                res['phone'] = phone
                res['contacts'] = contacts
                if res not in all_results[provider_name][product_name]:
                    all_results[provider_name][product_name].append(res)

            if break_out:
                break

        for provider_name, data in all_results.iteritems():
            file_name = u'%s-欧普钢网资源单-%s.xls'%(provider_name, today)
            file_path = os.path.join(gangyin_dir, file_name)

            wb = xlwt.Workbook()
            for product_name, rows in data.iteritems():
                r='[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+'
                product_name = re.sub(r,'',product_name)
                ws = wb.add_sheet(product_name)
                c = 2
                ws .write(0, 0 ,u'联系人:%s'%rows[0]['contacts'])
                ws.write(1, 0, u'电话：%s'%rows[0]['phone'])
                ws.write(c, 0, u'品名')
                ws.write(c, 1, u'牌号')
                ws.write(c, 2, u'规格')
                ws.write(c, 3, u'产地')
                ws.write(c, 4, u'仓库')
                ws.write(c, 5, u'重量')
                ws.write(c, 6, u'价格')
                # ws.write(c, 7, u'说明1')

                for row in rows:
                    c += 1
                    ws.write(c, 0, row['product_name'])
                    ws.write(c, 1, row['shop_sign'])
                    ws.write(c, 2, row['spec'])
                    ws.write(c, 3, row['manufacturer'])
                    ws.write(c, 4, row['warehouse_name'])
                    ws.write(c, 5, row['weight'])
                    ws.write(c, 6, row['price'])
                    # ws.write(c, 7, row['special'])

            wb.save(file_path)
            CrawlExcel.objects.create(
            create_time=time.time(),
            crawl_user=profile.user,
            source=7,
            # source_id=excel_id,
            filepath=file_path,
            provider=provider_name,
            imported=False
                    )
            print provider_name, file_path