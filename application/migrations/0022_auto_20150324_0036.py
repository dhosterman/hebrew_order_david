# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0021_auto_20150317_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='home_phone',
            field=models.CharField(blank=True, max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='mobile_phone',
            field=models.CharField(blank=True, max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='work_phone',
            field=models.CharField(blank=True, max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='wife',
            name='mobile_phone',
            field=models.CharField(blank=True, default='', max_length=20),
            preserve_default=False,
        ),
    ]
