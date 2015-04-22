# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excel', '0002_excel_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='excel',
            name='excel_file',
            field=models.FileField(upload_to=b'excels/%Y/%m/%d'),
        ),
    ]
