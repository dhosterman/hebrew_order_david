# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactDetails',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('home_address', models.CharField(max_length=255)),
                ('home_city', models.CharField(max_length=255)),
                ('home_state', models.CharField(default='TX', max_length=2)),
                ('home_zip', models.PositiveIntegerField()),
                ('postal_address', models.CharField(max_length=255)),
                ('postal_city', models.CharField(max_length=255)),
                ('postal_state', models.CharField(default='TX', max_length=2)),
                ('postal_zip', models.PositiveIntegerField()),
                ('home_phone', models.CharField(max_length=20)),
                ('work_phone', models.CharField(max_length=20)),
                ('mobile_phone', models.CharField(max_length=20)),
                ('fax', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('occupation', models.CharField(max_length=255)),
                ('business_name', models.CharField(max_length=255)),
                ('business_address', models.CharField(max_length=255)),
                ('business_city', models.CharField(max_length=255)),
                ('business_state', models.CharField(default='TX', max_length=2)),
                ('business_zip', models.PositiveIntegerField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OtherDetails',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('previous_member_of_hodi', models.BooleanField()),
                ('previous_lodges', models.CharField(max_length=255)),
                ('relatives_member_of_hodi', models.BooleanField()),
                ('relatives_names_and_mother_lodges', models.TextField()),
                ('member_of_other_organizations', models.BooleanField()),
                ('other_organizations', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonalDetails',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('date_of_birth', models.DateField()),
                ('city_of_birth', models.CharField(max_length=255)),
                ('country_of_birth', models.CharField(max_length=255)),
                ('is_jewish', models.BooleanField()),
                ('is_married', models.BooleanField()),
                ('date_of_marriage', models.DateField()),
                ('wife_name', models.CharField(max_length=255)),
                ('wife_email', models.EmailField(max_length=254)),
                ('place_of_marriage', models.CharField(max_length=255)),
                ('wife_mobile_phone', models.CharField(max_length=20)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
