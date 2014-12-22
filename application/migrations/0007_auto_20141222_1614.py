# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0006_auto_20141218_1524'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personaldetails',
            name='is_jewish',
        ),
        migrations.RemoveField(
            model_name='personaldetails',
            name='is_married',
        ),
        migrations.AlterField(
            model_name='personaldetails',
            name='city_of_birth',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='personaldetails',
            name='country_of_birth',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
    ]
