# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0010_auto_20150119_1555'),
    ]

    operations = [
        migrations.RenameField(
            model_name='otherdetails',
            old_name='previous_member_of_hodi',
            new_name='previous_member_of_hod',
        ),
        migrations.RenameField(
            model_name='otherdetails',
            old_name='relatives_member_of_hodi',
            new_name='relatives_member_of_hod',
        ),
    ]
