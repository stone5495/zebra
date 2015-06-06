# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HourBehaviour',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hour', models.CharField(max_length=15)),
                ('page_view', models.IntegerField()),
                ('user_view', models.IntegerField()),
                ('login_cnt', models.IntegerField()),
                ('search_cnt', models.IntegerField()),
                ('download_cnt', models.IntegerField()),
                ('register_cnt', models.IntegerField()),
                ('upload_cnt', models.IntegerField()),
                ('crawl_cnt', models.IntegerField()),
                ('record_date', models.DateField()),
                ('last_update_time', models.DateTimeField()),
            ],
            options={
                'ordering': ['-last_update_time'],
                'db_table': 'user_behaviour_hourly_static',
                'get_latest_by': 'last_update_time',
            },
        ),
    ]
