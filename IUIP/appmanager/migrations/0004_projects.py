# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-01 13:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appmanager', '0003_auto_20170701_1702'),
    ]

    operations = [
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.CharField(max_length=50, unique=True)),
                ('project_name', models.CharField(max_length=50, unique=True)),
                ('created_by', models.CharField(max_length=30)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_by', models.CharField(max_length=30)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('project_appid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appmanager.AppId')),
            ],
        ),
    ]
