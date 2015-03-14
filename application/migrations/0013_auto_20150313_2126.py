# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('application', '0012_auto_20150212_1658'),
    ]

    operations = [
        migrations.CreateModel(
            name='Children',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('hebrew_name', models.CharField(max_length=255)),
                ('date_of_birth', models.DateField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Committee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('home_address', models.CharField(max_length=255)),
                ('home_city', models.CharField(max_length=255)),
                ('home_state', models.CharField(max_length=2)),
                ('home_zip', models.PositiveIntegerField()),
                ('postal_same_as_home', models.BooleanField(default=True)),
                ('postal_address', models.CharField(blank=True, max_length=255)),
                ('postal_city', models.CharField(blank=True, max_length=255)),
                ('postal_state', models.CharField(blank=True, max_length=2)),
                ('postal_zip', models.PositiveIntegerField(blank=True, null=True)),
                ('home_phone', models.CharField(max_length=20)),
                ('work_phone', models.CharField(max_length=20)),
                ('mobile_phone', models.CharField(max_length=20)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Contact',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('synagogue_or_temple', models.CharField(blank=True, max_length=255)),
                ('sponsor', models.CharField(max_length=255)),
                ('sponsor_phone', models.CharField(max_length=20)),
                ('previous_member_of_hod', models.BooleanField(verbose_name='Previous member of HOD', default=False)),
                ('previous_lodges', models.CharField(blank=True, max_length=255)),
                ('skills_or_hobbies', models.TextField(blank=True)),
                ('other_organizations', models.TextField(blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Legal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('terms_and_conditions', models.TextField()),
                ('privacy_policy', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Occupation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('occupation', models.CharField(max_length=255)),
                ('business_name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=2)),
                ('zip', models.PositiveIntegerField()),
                ('phone', models.CharField(max_length=20)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Personal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_of_birth', models.DateField()),
                ('city_of_birth', models.CharField(max_length=255)),
                ('country_of_birth', models.CharField(max_length=255)),
                ('married', models.BooleanField(default=False)),
                ('children', models.BooleanField(default=False)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Personal',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserCommittee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('current', models.BooleanField(default=False)),
                ('years', models.PositiveIntegerField()),
                ('committee', models.ForeignKey(to='application.Committee')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Wife',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('hebrew_name', models.CharField(blank=True, max_length=255)),
                ('date_of_birth', models.DateField(null=True)),
                ('email', models.EmailField(blank=True, max_length=75)),
                ('mobile_phone', models.CharField(blank=True, max_length=20)),
                ('date_of_marriage', models.DateField(blank=True)),
                ('country_of_marriage', models.CharField(blank=True, max_length=255)),
                ('city_of_marriage', models.CharField(blank=True, max_length=255)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='contactdetails',
            name='user',
        ),
        migrations.DeleteModel(
            name='ContactDetails',
        ),
        migrations.RemoveField(
            model_name='otherdetails',
            name='user',
        ),
        migrations.DeleteModel(
            name='OtherDetails',
        ),
        migrations.RemoveField(
            model_name='personaldetails',
            name='user',
        ),
        migrations.DeleteModel(
            name='PersonalDetails',
        ),
        migrations.AddField(
            model_name='committee',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='application.UserCommittee'),
            preserve_default=True,
        ),
    ]
