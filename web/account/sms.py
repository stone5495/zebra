#coding=utf-8

import httplib
import urllib
import json


API_KEY = '4397914c284e758ae2eff1e5bc35c826'

sms_tpl_send_uri = '/v1/sms/tpl_send.json'


def tpl_send_sms(apikey, tpl_id, tpl_value, mobile):
    """
    模板接口发短信
    """
    params = urllib.urlencode({'apikey': apikey, 'tpl_id':tpl_id, 'tpl_value': tpl_value, 'mobile':mobile})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection('yunpian.com', port=80, timeout=30)
    conn.request("POST", sms_tpl_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str


def send_validation_code(phone, code):
    result = tpl_send_sms(API_KEY, 1, '#code#=%s&#company#=斑马搜索' % code, phone)
    code = json.loads(result)['code']
    if code != 0:
        raise Exception(result)