#coding=utf-8

from django.core.management import BaseCommand
from django.conf import settings

from selenium import webdriver
from pyquery.pyquery import PyQuery as pq

import os, datetime, time
import requests, urllib, redis

from excel.models import CrawlExcel


url = 'http://zy.banksteel.com/?bi=&bd=&ci=&cy=&br=&kw=&st=6&'
download_url = 'http://zy.banksteel.com/d/%s'

driver = webdriver.PhantomJS()


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        print '开始下载钢银网资源单...'

        if not os.path.exists(settings.CRAWL_ROOT):
            os.mkdir(settings.CRAWL_ROOT)
            print '新建目录: %s' % settings.CRAWL_ROOT

        today = datetime.datetime.now().strftime('%Y_%m_%d')
        today_dir = os.path.join(settings.CRAWL_ROOT, today)

        if not os.path.exists(today_dir):
            os.mkdir(today_dir)
            print '新建目录: %s' % today_dir

        gangyin_dir = os.path.join(today_dir, 'gangyin')
        if not os.path.exists(gangyin_dir):
            os.mkdir(gangyin_dir)
            print '新建目录: %s' % gangyin_dir

        driver.get(url)
        time.sleep(2)
        q = pq(driver.page_source)
        pages = q('.page').text()[25:33]
        pages = int(filter(lambda x: x in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], pages))

        print '一共%d页' % pages

        for page in range(1, pages+1):
            driver.get(url+'pg=%d'%page)
            print '第%d页' % page
            time.sleep(2)
            # import pdb
            # pdb.set_trace()
            q = pq(driver.page_source)
            q = q('table tr')

            for _ in q[3:]:
                # import pdb
                # pdb.set_trace()
                excel_id = pq(pq(_).find('a')[-2]).attr('href').split('/')[-1]

                if CrawlExcel.objects.filter(source=2, source_id=excel_id).exists():
                    continue

                try:
                    r = requests.get(download_url % excel_id, stream=True)
                    file_name = urllib.unquote(r.headers['content-disposition'].split('=')[1]).decode('gbk').encode('utf-8')

                    print '下载中: [%s] %s' % (excel_id, file_name)
                    file_path = os.path.join(gangyin_dir, file_name)

                    f = open(file_path, 'wb')
                    for block in r.iter_content(1024):
                        if not block:
                            break
                        f.write(block)
                    f.close()

                    CrawlExcel.objects.create(
                        create_time=time.time(),
                        source=2,
                        source_id=excel_id,
                        filepath=file_path,
                        imported=False
                    )

                except Exception as e:
                    print '错误: [%s]' % excel_id
                    import traceback
                    traceback.print_exc()
