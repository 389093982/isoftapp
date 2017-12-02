# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models

# Create your models here.


class ExcludeDispatch(models.Model):
    task_type = models.CharField(max_length=50)
    task_name = models.CharField(max_length=150)
    exclude_from_time = models.DateTimeField()
    exclude_end_time = models.DateTimeField()
    created_by = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.CharField(max_length=30)
    last_updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'exclude_dispatch_t'


class CronMeta(models.Model):
    task_type = models.CharField(max_length=50)
    task_name = models.CharField(max_length=50)
    second = models.CharField(max_length=50, default='*')
    minute = models.CharField(max_length=50, default='*')
    hour = models.CharField(max_length=50, default='*')
    day = models.CharField(max_length=50, default='*')
    month = models.CharField(max_length=50, default='*')
    day_of_week = models.CharField(max_length=50, default='*')
    year = models.CharField(max_length=50, default='*')
    created_by = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.CharField(max_length=30)
    last_updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'quartz_cron_meta_t'

class SchedulerLog(models.Model):
    job_id = models.CharField(max_length=200)
    task_type = models.CharField(max_length=100)
    task_name = models.CharField(max_length=100)
    destination = models.CharField(max_length=50)
    created_by = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.CharField(max_length=30)
    last_updated_date = models.DateTimeField(auto_now=True)

class ExcludeDispatchAdmin(admin.ModelAdmin):
    pass

class CronMetaAdmin(admin.ModelAdmin):
    pass

class SchedulerLogAdmin(admin.ModelAdmin):
    list_display = ('job_id', 'task_type', 'task_name', 'destination')

admin.site.register(ExcludeDispatch, ExcludeDispatchAdmin)
admin.site.register(CronMeta, CronMetaAdmin)
admin.site.register(SchedulerLog, SchedulerLogAdmin)