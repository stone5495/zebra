#coding=utf-8

from common.apis.es import es, es_rest_call
import time, datetime


def get_index_name():
    today = datetime.datetime.today()
    return 'datapoint_%s_%s_%s'%(today.year, today.month, today.day)


def record_data_point(request, action, **kwargs):
    now = time.time()

    ip = request.META['HTTP_X_FORWARDED_FOR'] if 'HTTP_X_FORWARDED_FOR' in request.META else request.META['REMOTE_ADDR']
    data = {
        'time': now,
        'ip': ip,
        'user': request.user.phoneuserprofile.phone if request.user.is_authenticated() and not request.user.is_staff else ''
    }
    data.update(kwargs)

    index_name = get_index_name()

    try:
        es_rest_call('/%s'%index_name, 'PUT')
    except:
        pass

    es.index(index_name, action, data)
