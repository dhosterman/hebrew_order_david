# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0019_auto_20150316_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercommittee',
            name='position',
            field=models.CharField(blank=True, max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usercommittee',
            name='years',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
    ]
