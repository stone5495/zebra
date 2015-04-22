#coding=utf-8
from django.core.management import BaseCommand
from django.conf import settings

from common.apis.es import es, es_rest_call


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        index = 'excel'

        body = {
            "mappings" : {
                "excel_file" : {},
                "row_data" : {
                    "_parent" : {
                      "type" : "excel_file"
                    }
                }
            }
        }

        try:
            es_rest_call('/%s'%index, 'DELETE')
            es_rest_call('/%s'%index, 'PUT', body)
        except:
            es_rest_call('/%s'%index, 'PUT', body)
        
        print '索引已建'


