# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-11 15:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quartz', '0002_auto_20171111_2300'),
    ]

    operations = [
        migrations.RenameField(
            model_name='excludedispatch',
            old_name='exclude_name',
            new_name='task_name',
        ),
        migrations.RenameField(
            model_name='excludedispatch',
            old_name='type_name',
            new_name='task_type',
        ),
    ]
