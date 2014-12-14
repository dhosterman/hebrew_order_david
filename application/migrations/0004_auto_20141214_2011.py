# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0003_otherdetails_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactdetails',
            name='business_address',
            field=models.CharField(blank=True, max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='business_city',
            field=models.CharField(blank=True, max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='business_name',
            field=models.CharField(blank=True, max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='business_state',
            field=models.CharField(blank=True, max_length=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='business_zip',
            field=models.PositiveIntegerField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='fax',
            field=models.CharField(blank=True, max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='home_address',
            field=models.CharField(blank=True, max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='home_city',
            field=models.CharField(blank=True, max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='home_phone',
            field=models.CharField(blank=True, max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='home_state',
            field=models.CharField(blank=True, max_length=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='home_zip',
            field=models.PositiveIntegerField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='mobile_phone',
            field=models.CharField(blank=True, max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='occupation',
            field=models.CharField(blank=True, max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='postal_address',
            field=models.CharField(blank=True, max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='postal_city',
            field=models.CharField(blank=True, max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='postal_state',
            field=models.CharField(blank=True, max_length=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='postal_zip',
            field=models.PositiveIntegerField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='work_phone',
            field=models.CharField(blank=True, max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='otherdetails',
            name='other_organizations',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='otherdetails',
            name='previous_lodges',
            field=models.CharField(blank=True, max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='otherdetails',
            name='relatives_names_and_mother_lodges',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='personaldetails',
            name='city_of_birth',
            field=models.CharField(blank=True, max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='personaldetails',
            name='country_of_birth',
            field=models.CharField(blank=True, max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='personaldetails',
            name='date_of_marriage',
            field=models.DateField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='personaldetails',
            name='place_of_marriage',
            field=models.CharField(blank=True, max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='personaldetails',
            name='wife_email',
            field=models.EmailField(blank=True, max_length=254),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='personaldetails',
            name='wife_mobile_phone',
            field=models.CharField(blank=True, max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='personaldetails',
            name='wife_name',
            field=models.CharField(blank=True, max_length=255),
            preserve_default=True,
        ),
    ]
