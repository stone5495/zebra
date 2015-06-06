# -*- coding: utf-8 -*-
from django.http import HttpResponse


def generate_excel(filename):

    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename={}.xls'.format(filename)
    return response
