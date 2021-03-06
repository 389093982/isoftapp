# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-09 14:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IntgList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('integration_point_name', models.CharField(max_length=150)),
                ('integration_point_version', models.CharField(max_length=20)),
                ('env_name', models.CharField(max_length=50)),
                ('status', models.IntegerField()),
                ('source_client_name', models.CharField(max_length=50)),
                ('target_client_name', models.CharField(max_length=50)),
                ('created_by', models.CharField(max_length=30)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_by', models.CharField(max_length=30)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'integration_point_list_t',
            },
        ),
    ]
