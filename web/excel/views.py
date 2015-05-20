#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.views import serve

from models import Excel
from common.apis.es import es
import time, xlrd


def search(request):
    q = request.GET.get('q', '')

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
            "_score",
            {
                "time": "desc"
            }
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

    return HttpResponseRedirect('/index/%d'%excel.id)


def index_excel(excel):
    wb = xlrd.open_workbook(excel.excel_file.file.name)

    doc = es.index('excel', 'excel_file', {
        'id': excel.id,
        'name': excel.name,
        'time': excel.create_time,
        'phone': excel.user.phoneuserprofile.phone,
        'nickname': excel.user.phoneuserprofile.nickname,
    }, id=excel.id)

    for sheet_index in range(wb.nsheets):
        sheet = wb.sheet_by_index(sheet_index)

        for row_index in range(sheet.nrows):
            values = []
            for col_index in range(sheet.ncols):
                try:
                    value = sheet.cell_value(row_index, col_index)
                    if value:
                        values.append(unicode(value))
                except:
                    pass

            if not values:
                continue

            es.index('excel', 'row_data', {
                'parent': doc['_id'],
                'time': excel.create_time,
                'sheet': sheet_index,
                'sheet_name': sheet.name,
                'row': row_index,
                'cell': values
            }, parent=doc['_id'])

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
    return HttpResponseRedirect('/manage/')


def download(request, excel_id):
    try:
        excel = Excel.objects.get(id=excel_id)
    except Excel.DoesNotExist:
        return HttpResponse(u'Excel不存在', status=404)

    #添加下载记录

    return HttpResponseRedirect(excel.excel_file.url)


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

    return render(request, 'detail.html', excel_data)


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


