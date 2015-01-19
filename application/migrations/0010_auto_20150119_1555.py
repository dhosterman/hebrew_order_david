# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0009_auto_20141231_2343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personaldetails',
            name='date_of_marriage',
            field=models.DateField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
