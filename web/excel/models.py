#coding=utf-8
from django.db import models
from django.contrib.auth.models import User


class Excel(models.Model):
    create_time = models.FloatField()
    user = models.ForeignKey(User)

    name = models.CharField(max_length=100)
    provider = models.CharField(max_length=100)

    excel_file = models.FileField(upload_to='excels/%Y/%m/%d')
    status = models.IntegerField()


class Record(models.Model):
    time = models.FloatField()
    user = models.ForeignKey(User)

    excel = models.ForeignKey(Excel)
    query = models.CharField(max_length=100)
    download = models.BooleanField()


class CrawlExcel(models.Model):
    create_time = models.FloatField()
    crawl_user = models.ForeignKey(User)

    source = models.IntegerField()
    source_id = models.CharField(max_length=50)
    filepath = models.CharField(max_length=255)

    provider = models.CharField(max_length=100)
    imported = models.BooleanField()