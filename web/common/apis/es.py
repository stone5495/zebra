#coding=utf8
from elasticsearch import Elasticsearch, exceptions
from django.conf import settings

from json import dumps


###################### Elastic Search 调用接口 ################

es = Elasticsearch(settings.ES_SERVER) # ES 官方的python客户端，可以调用一些基本方法
es_debug = False


def es_rest_call(url='/', method='GET', body=None):
    """
    用restful方式调用ES, 用来调用未写入官方客户端的方法

    @param url: 地址，相对路径
    @param method: HTTP方法，相当于CURL当中的-XGET XPOST XDELETE XPUT
    @param body: post时传入的参数对象
    @return: 成功返回服务器response，失败抛异常
    """

    if es_debug:
        print '='*20+'   ES call BEGIN   '+'='*20
        print 'req ==> [%s] http://%s%s, %s' % (method, settings.ES_SERVER, url, dumps(body, indent=2))

    status_code, response = es.transport.perform_request(method, url, None, body)

    if es_debug:
        print 'status_code <== %s' % status_code
        print 'res <== %s' % dumps(response, indent=2)
        print '='*20+'   ES call END   '+'='*20


    if 200 <= status_code < 300:
        return response

    raise Exception({
        'status_code': status_code,
        'response': response
    })
