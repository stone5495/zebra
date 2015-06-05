# coding=utf-8

from django.db import models


class HourBehaviour(models.Model):

    hour = models.CharField(MaxLenth=15)

    page_view = models.IntegerField()
    user_view = models.IntegerField()
    search_count = models.IntegerField()
    download_count = models.IntegerField()
    register_count = models.IntegerField()
    upload_count = models.IntegerField()
    crawl_count = models.IntegerField()

    last_update_tim = models.DateTimeField()
