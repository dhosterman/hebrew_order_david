# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0016_auto_20150315_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='children',
            name='name',
            field=models.CharField(blank=True, max_length=255),
            preserve_default=True,
        ),
    ]
