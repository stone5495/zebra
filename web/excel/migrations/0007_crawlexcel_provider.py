# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excel', '0006_crawlexcel_crawl_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='crawlexcel',
            name='provider',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
