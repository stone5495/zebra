#coding=utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.views import serve

from models import Excel
from common.apis.es import es
from ubt.datapoint import record_data_point
import time, xlrd, re, uuid, json

from suds.client import Client


def home(request):
    return render(request, 'home.html', {})


def search(request):
    q = request.GET.get('q', '')
    if not q:
        return redirect('/')

    record_data_point(request, 'search', q=q)

    hits = []
    docs = {}
    target_start = 0
    target_end = 20

    start = 0
    count = 50

    query_dict = {
        "query": {
            "query_string": {
                "query": q
            }
        },
        "sort": [
            "_score"
        ]
    }

    while len(hits) < target_end:
        query_dict['from'] = start
        query_dict['size'] = count

        result = es.search('excel', 'row_data', query_dict)
        start += count

        if not result['hits']['hits']:
            break

        for _ in result['hits']['hits']:
            parent = _['_source']['parent']
            if parent not in hits:
                hits.append(parent)
                docs[parent] = [_['_source']]
            else:
                docs[parent].append(_['_source'])

    if not hits[target_start:target_end]:
        result = []

    else:
        excels = es.mget({
            'ids': hits[target_start:target_end]
        }, 'excel', 'excel_file')['docs']

        result = [{
            'excel': _['_source'],
            'rows': docs[_['_id']][:8]
        } for _ in excels]

    template_context = {
        'search_result': result,
        'q': q
    }

    return render(request, 'search.html', template_context)


@login_required
def upload(request):
    excel_file = request.FILES['excel_file']

    excel = Excel.objects.create(
        create_time = time.time(),
        user = request.user,
        name = excel_file.name,
        status = 0,
        excel_file = excel_file
    )

    record_data_point(request, 'upload', excel_id=excel.id)

    return HttpResponseRedirect('/index/%d'%excel.id)


def analyze_spec(v):
    m = re.match(u'\s*(\d+(\.\d+)?)\*(\d+(\.\d+)?)', v)
    if m:
        return {
            'thick': m.groups()[0],
            'width': m.groups()[2],
            'spec': v.strip()
        }


def analyze_warehouse(v):
    m = re.match(u'\s*(.*[库厂豪源工流号(储运有限公司)])', v)
    if m:
        return {
            'warehouse': v
        }


def analyze_weight(v):
    t = v.strip()

    m = re.match(u'\s*(\d{1,3}\.\d+?)\s*', v)
    if m:
        return {
            'weight': v
        }


analyzers = [analyze_spec, analyze_warehouse, analyze_weight]


def index_excel(excel):
    wb = xlrd.open_workbook(excel.excel_file.file.name)

    doc = es.index('excel', 'excel_file', {
        'id': excel.id,
        'name': excel.name,
        'time': excel.create_time,
        'provider': excel.provider,
        'phone': excel.user.phoneuserprofile.phone,
        'nickname': excel.user.phoneuserprofile.nickname,
    }, id=excel.id)

    for sheet_index in range(wb.nsheets):
        sheet = wb.sheet_by_index(sheet_index)

        for row_index in range(sheet.nrows):
            values = []

            extends = {}

            for col_index in range(sheet.ncols):
                try:
                    value = sheet.cell_value(row_index, col_index)
                    if value:
                        values.append(unicode(value))
                        for analyzer in analyzers:
                            analyze_dict = analyzer(unicode(value))
                            if analyze_dict:
                                extends.update(analyze_dict)
                except:
                    pass

            if not values:
                continue

            d = {
                'parent': doc['_id'],
                'time': excel.create_time,
                'sheet': sheet_index,
                'sheet_name': sheet.name,
                'row': row_index,
                'cell': values            
            }
            d.update(extends)
            es.index('excel', 'row_data', d, parent=doc['_id'])

    excel.status = 1
    excel.save()


@login_required
def index(request, excel_id):
    try:
        excel = Excel.objects.get(id=excel_id)
    except Excel.DoesNotExist:
        return HttpResponse(u'Excel不存在', status=404)

    if request.user != excel.user:
        return HttpResponse(u'Excel不属于你', status=401)        

    if excel.status == 1:
        return HttpResponse(u'已经索引过了', status=403)

    index_excel(excel)
    record_data_point(request, 'index', excel_id=excel.id)
    return HttpResponseRedirect('/manage/')


def unindex_excel(excel):
    es.delete_by_query('excel', 'row_data', {
        'query': {
            'term': {
                'parent': excel.id
            }
        }
    })

    es.delete('excel', 'excel_file', id=excel.id)

    excel.status = 0
    excel.save()


@login_required
def unindex(request, excel_id):
    try:
        excel = Excel.objects.get(id=excel_id)
    except Excel.DoesNotExist:
        return HttpResponse(u'Excel不存在', status=404)

    if request.user != excel.user:
        return HttpResponse(u'Excel不属于你', status=401)        

    if excel.status == 0:
        return HttpResponse(u'本来就不在索引中', status=403)

    unindex_excel(excel)
    record_data_point(request, 'unindex', excel_id=excel.id)

    return HttpResponseRedirect('/manage/')


@login_required
def download(request, excel_id):
    try:
        excel = Excel.objects.get(id=excel_id)
    except Excel.DoesNotExist:
        return HttpResponse(u'Excel不存在', status=404)

    #添加下载记录
    download = request.GET.get('file', '')

    if download:
        record_data_point(request, 'download', excel_id=excel.id)
        return HttpResponseRedirect(excel.excel_file.url)
    else:
        return render(request, 'download.html', { 'excel_id': excel_id })


def detail(request, excel_id):
    try:
        excel = Excel.objects.get(id=excel_id)
    except Excel.DoesNotExist:
        return HttpResponse(u'Excel不存在', status=404)

    wb = xlrd.open_workbook(excel.excel_file.file.name)

    excel_data = {
        'name': excel.name,
        'id': excel.id,
        'name': excel.name,
        'time': excel.create_time,
        'phone': excel.user.phoneuserprofile.phone,
        'nickname': excel.user.phoneuserprofile.nickname,
        'sheets': []
    }

    for sheet_index in range(wb.nsheets):
        sheet = wb.sheet_by_index(sheet_index)
        sheet_data = {
            'name': sheet.name,
            'num': sheet_index,
            'rows': []
        }
        excel_data['sheets'].append(sheet_data)

        for row_index in range(sheet.nrows):
            row_data = {
                'line': row_index,
                'cells': []
            }
            for col_index in range(sheet.ncols):
                try:
                    value = sheet.cell_value(row_index, col_index)
                    if value:
                        row_data['cells'].append(unicode(value))
                except:
                    pass

            if row_data['cells']:
                sheet_data['rows'].append(row_data)

    record_data_point(request, 'detail', excel_id=excel_id)
    return render(request, 'detail.html', excel_data)


def get_warehouse_code(warehouse_name):
    query_dict = {
        "query": {
            "query_string": {
                "query": warehouse_name
            }
        },
        "sort": [
            "_score"
        ]
    }
    result = es.search('excel', 'warehouse', query_dict)['hits']['hits']
    if not result: return

    top = result[0]
    if top['_score'] < 1.0:
        return

    return top['_source']['code']


def check_good(warehouse_code, provider_name, thick, width, weight):
    url = 'http://wms.baosaas.com/STMTOBYTSERVICE_NEW/StmToBytService.asmx?wsdl'
    client = Client(url)
    client.set_options(soapheaders=None)
    header = client.factory.create('ServiceSoapHeader')
    header.UserToken ='Welcome2BYT'
    client.set_options(soapheaders=header)

    request = client.factory.create('ArrayOfCheckGoodsModel')
    
    req_item = client.factory.create('CheckGoodsModel')
    req_item.requestSn = 'sn_'+uuid.uuid1().hex
    req_item.sysId = 'STM06'
    req_item.deptId = warehouse_code
    req_item.packNum = ''
    req_item.resourceNum = ''
    req_item.netWeight = weight
    req_item.wproviderId = ''
    req_item.wproviderName = u''
    req_item.providerId = ''
    req_item.providerName = provider_name
    req_item.kindNo = ''
    req_item.kindName = u''
    req_item.shopSignName = ''
    req_item.prodareaName = u''
    req_item.gradenumThick = thick
    req_item.gradenumWidth = width
    req_item.gradenumLength = '0'
    req_item.goodId = '1'
    req_item.planQty = ''
    req_item.businessType = ''
    req_item.goodsId = ''
    req_item.ownerId = ''
    req_item.spec = ''
    req_item.ruleType = 'A'
    req_item.checkRules = '90'

    request.CheckGoodsModel.append(req_item)
    resp = client.service.stmToBytCheckGoods(request)

    if hasattr(resp, 'checkResponseResult'):
        result = resp.checkResponseResult.ResultCheckGoods
    else:
        result = resp.ResultCheckGoods

    return {
        'code': result[0]['returnCode'],
        'msg': result[0]['returnMsg']
    }


def check_resource(request):
    warehouse_name = request.GET['warehouse_name']
    provider_name = request.GET['provider_name']
    thick = request.GET['thick']
    width = request.GET['width']
    weight = request.GET['weight']

    warehouse_code = get_warehouse_code(warehouse_name)
    if not warehouse_code:
        return HttpResponse(u'未找到仓库', status=404)

    result = check_good(warehouse_code, provider_name, thick, width, weight)
    record_data_point(request, 'check_good', 
        warehouse_name=warehouse_name, provider_name=provider_name,
        thick=thick, width=width, weight=weight)
    return HttpResponse(json.dumps(result, indent=2))


@login_required
def ask(request):
    return HttpResponse(0)


@login_required
def record(request):
    return HttpResponse(0)


@login_required
def manage(request):
    excels = Excel.objects.filter(user=request.user)

    context = {
        'indexed_excels': excels.filter(status=1),
        'unindexed_excels': excels.filter(status=0),
    }
    return render(request, 'manage.html', context)


