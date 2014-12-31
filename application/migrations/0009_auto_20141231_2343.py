# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0008_auto_20141231_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactdetails',
            name='postal_zip',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
