# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from application.models import Legal

def add_legal_text(apps, schema_editor):
    legal = Legal.objects.get_or_create(pk=1)
    if legal[1]:
        legal = legal[0]
        legal.terms_and_conditions = 'I declare that all information above is true to the best of my knowledge. I am a duly initiated member of HOD international, Lodge Shimon Peres, Dallas Texas, in good standing, and agree to abide by all rules, regulations and traditions of HOD International and the Lodge.'
        legal.privacy_policy = 'The information contained on this form is for HOD International purposes only and will never be sold or shared outside the HOD without prior permission from the Member.'
        legal.save()

class Migration(migrations.Migration):

    dependencies = [
        ('application', '0017_auto_20150316_1914'),
    ]

    operations = [
        migrations.RunPython(add_legal_text),
    ]
