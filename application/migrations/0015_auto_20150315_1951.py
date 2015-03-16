# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0014_usercommittee_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wife',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='wife',
            name='date_of_marriage',
            field=models.DateField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
