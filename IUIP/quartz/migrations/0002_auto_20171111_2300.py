# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-11 15:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quartz', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cronmeta',
            name='day',
            field=models.CharField(default='*', max_length=50),
        ),
        migrations.AlterField(
            model_name='cronmeta',
            name='day_of_week',
            field=models.CharField(default='*', max_length=50),
        ),
        migrations.AlterField(
            model_name='cronmeta',
            name='hour',
            field=models.CharField(default='*', max_length=50),
        ),
        migrations.AlterField(
            model_name='cronmeta',
            name='minute',
            field=models.CharField(default='*', max_length=50),
        ),
        migrations.AlterField(
            model_name='cronmeta',
            name='month',
            field=models.CharField(default='*', max_length=50),
        ),
        migrations.AlterField(
            model_name='cronmeta',
            name='second',
            field=models.CharField(default='*', max_length=50),
        ),
        migrations.AlterField(
            model_name='cronmeta',
            name='year',
            field=models.CharField(default='*', max_length=50),
        ),
    ]
