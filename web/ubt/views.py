# -*- coding: utf-8 -*-


from django.shortcuts import render
from handlers.overview import OverView


def overview(request, params):
    profile = OverView(request)
    try:
        func = getattr(profile, "get_{}".format(params))
    except Exception as err:
        return render(request, "overview.html")
    return func()


