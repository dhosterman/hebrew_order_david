# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0013_auto_20150313_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercommittee',
            name='position',
            field=models.CharField(max_length=255, default=''),
            preserve_default=False,
        ),
    ]
