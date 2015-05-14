# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_phoneuserprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='phoneuserprofile',
            name='status',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
