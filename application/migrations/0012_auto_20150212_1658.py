# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0011_auto_20150212_1646'),
    ]

    operations = [
        migrations.RenameField(
            model_name='personaldetails',
            old_name='place_of_marriage',
            new_name='country_where_married',
        ),
        migrations.AddField(
            model_name='otherdetails',
            name='sponsor',
            field=models.CharField(max_length=255, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='otherdetails',
            name='previous_member_of_hod',
            field=models.BooleanField(default=False, verbose_name='Previous member of HOD'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='otherdetails',
            name='relatives_member_of_hod',
            field=models.BooleanField(default=False, verbose_name='Relatives member of HOD'),
            preserve_default=True,
        ),
    ]
