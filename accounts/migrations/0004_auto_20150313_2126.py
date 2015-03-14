# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20141215_0248'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='hebrew_name',
            field=models.CharField(default='', blank=True, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
    ]
