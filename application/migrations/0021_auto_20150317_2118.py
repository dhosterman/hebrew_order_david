# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0020_auto_20150317_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercommittee',
            name='committee',
            field=models.ForeignKey(null=True, to='application.Committee'),
            preserve_default=True,
        ),
    ]
