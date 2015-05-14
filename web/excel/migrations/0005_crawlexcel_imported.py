# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excel', '0004_crawlexcel'),
    ]

    operations = [
        migrations.AddField(
            model_name='crawlexcel',
            name='imported',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
