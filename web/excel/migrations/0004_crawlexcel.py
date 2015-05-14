# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excel', '0003_auto_20150422_0656'),
    ]

    operations = [
        migrations.CreateModel(
            name='CrawlExcel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.FloatField()),
                ('source', models.IntegerField()),
                ('source_id', models.CharField(max_length=50)),
                ('filepath', models.CharField(max_length=255)),
            ],
        ),
    ]
