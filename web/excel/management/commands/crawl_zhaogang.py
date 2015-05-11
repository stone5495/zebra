#coding=utf-8

from django.core.management import BaseCommand
from django.conf import settings

from selenium import webdriver
from pyquery.pyquery import PyQuery as pq

import os, datetime, time
import requests, urllib, redis


url = 'http://zyd.zhaogang.com/ziyuan.html'
download_url = 'http://zyddownload.zhaogang.com/Ajax/DownLoad/ZydDownLoad.ashx?callback=?&PKID=%s'

driver = webdriver.PhantomJS()


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        print '开始下载找钢网资源单...'

        if not os.path.exists(settings.CRAWL_ROOT):
            os.mkdir(settings.CRAWL_ROOT)
            print '新建目录: %s' % settings.CRAWL_ROOT

        today = datetime.datetime.now().strftime('%Y_%m_%d')
        today_dir = os.path.join(settings.CRAWL_ROOT, today)

        if not os.path.exists(today_dir):
            os.mkdir(today_dir)
            print '新建目录: %s' % today_dir

        zhaogang_dir = os.path.join(today_dir, 'zhaogang')
        if not os.path.exists(zhaogang_dir):
            os.mkdir(zhaogang_dir)
            print '新建目录: %s' % zhaogang_dir

        update_file = os.path.join(zhaogang_dir, '.update')
        uf = file(update_file, 'a')
        uf.write('%lf'%time.time())
        uf.write('\n')

        driver.get(url)
        time.sleep(2)
        q = pq(driver.page_source)
        pages = int(q('.total').text()[1:-1])
        print '一共%d页' % pages

        for page in range(1, pages+1):
            driver.get(url+'?p=%d'%page)
            print '第%d页' % page
            time.sleep(2)
            q = pq(driver.page_source)
            q = q('table tr')

            for _ in q[1:]:
                excel_id = pq(pq(_).find('a')[-2]).attr('vals')
                lock_file = os.path.join(zhaogang_dir, '.'+excel_id)

                if os.path.exists(lock_file):
                    continue

                try:
                    r = requests.get(download_url % excel_id, stream=True)
                    file_name = urllib.unquote(r.headers['content-disposition'].split('=')[1])

                    print '下载中: [%s] %s' % (excel_id, file_name)
                    file_path = os.path.join(zhaogang_dir, file_name)

                    f = open(file_path, 'wb')
                    for block in r.iter_content(1024):
                        if not block:
                            break
                        f.write(block)
                    f.close()

                    lf = open(lock_file, 'w')
                    lf.write(file_name)
                    lf.close()

                    uf.write(excel_id)
                    uf.write(' ')

                except Exception as e:
                    print '错误: [%s]' % excel_id
                    import traceback
                    traceback.print_exc()

        uf.write('\n')
        uf.close()

