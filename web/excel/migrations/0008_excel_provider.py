# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excel', '0007_crawlexcel_provider'),
    ]

    operations = [
        migrations.AddField(
            model_name='excel',
            name='provider',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
