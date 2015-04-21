# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ValidationCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.FloatField()),
                ('expire_time', models.FloatField()),
                ('code', models.CharField(max_length=4)),
                ('phone', models.CharField(max_length=11)),
                ('status', models.IntegerField()),
            ],
        ),
    ]
