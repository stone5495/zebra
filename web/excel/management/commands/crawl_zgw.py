#coding=utf-8

from django.core.management import BaseCommand
from django.conf import settings

from selenium import webdriver
from pyquery.pyquery import PyQuery as pq

import os, datetime, time
import requests, urllib, redis

from excel.models import CrawlExcel



url = 'http://www.zgw.com/ProductResource/Download'
download_url = 'http://www.zgw.com/product/ExcelExport?epId=%s'

driver = webdriver.PhantomJS()


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        print '开始下载中钢网资源单...'

        if not os.path.exists(settings.CRAWL_ROOT):
            os.mkdir(settings.CRAWL_ROOT)
            print '新建目录: %s' % settings.CRAWL_ROOT

        today = datetime.datetime.now().strftime('%Y_%m_%d')
        today_dir = os.path.join(settings.CRAWL_ROOT, today)

        if not os.path.exists(today_dir):
            os.mkdir(today_dir)
            print '新建目录: %s' % today_dir

        zhonggang_dir = os.path.join(today_dir, 'zhonggang')
        if not os.path.exists(zhonggang_dir):
            os.mkdir(zhonggang_dir)
            print '新建目录: %s' % zhonggang_dir

        driver.get(url)
        time.sleep(2)
        q = pq(driver.page_source)
        # import pdb
        # pdb.set_trace()
        pages = int(q('.pagenum').text()[1:-5])
        print '一共%d页' % pages

        for page in range(1, pages+1):
            driver.get(url+'?page=%d'%page)
            print '第%d页' % page
            time.sleep(2)
            q = pq(driver.page_source)
            q = q('table tr ')

            for _ in q[1:]:
                excel_id = str(pq(pq(_).find('td')[0]).attr('id'))

                if excel_id == 'None':
                    continue

                if CrawlExcel.objects.filter(source=2, source_id=excel_id).exists():
                    continue

                try:
                    r = requests.get(download_url % excel_id, stream=True)
                    file_name = urllib.unquote(r.headers['content-disposition'].split('=')[1])

                    print '下载中: [%s] %s' % (excel_id, file_name)
                    file_path = os.path.join(zhonggang_dir, file_name)

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
