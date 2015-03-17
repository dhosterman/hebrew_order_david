# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from application.models import Committee

def add_committees(apps, schema_editor):
    committees = [
        'Fundraising and Social Action',
        'Membership',
        'Social Functions',
        'Archivist and Historian',
        'Treasury',
        'Communication and Social Media',
        'Executive Committee'
    ]

    for committee in committees:
        c = Committee(name=committee)
        c.save()

class Migration(migrations.Migration):

    dependencies = [
        ('application', '0018_auto_20150316_1920'),
    ]

    operations = [
        migrations.RunPython(add_committees),
    ]
