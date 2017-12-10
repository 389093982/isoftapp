# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib import admin
from django.db import models


# Create your models here.

class IntgList(models.Model):
    '''
    集成点清单表
    '''
    integration_point_name = models.CharField(max_length=150)
    integration_point_version = models.CharField(max_length=20)
    env_name = models.CharField(max_length=50)
    status = models.IntegerField()  # 0 草稿状态
    source_client_name = models.CharField(max_length=50)
    target_client_name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    created_by = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.CharField(max_length=30)
    last_updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'integration_point_list_t'
        # 联合主键
        unique_together = ('integration_point_name', 'integration_point_version')


class TimerIntgPoint(models.Model):
    '''
    定时集成点主表
    '''
    integration_point_name = models.CharField(max_length=150)
    integration_point_version = models.CharField(max_length=20)
    env_name = models.CharField(max_length=50)
    integration_point_status = models.IntegerField()
    source_db_conn = models.CharField(max_length=100)
    target_db_conn = models.CharField(max_length=100)
    source_client_name = models.CharField(max_length=50)
    target_client_name = models.CharField(max_length=50)
    migrate_begin_time = models.DateTimeField(default=datetime(1970, 1, 1, 00, 00, 00))
    created_by = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.CharField(max_length=30)
    last_updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'timer_integration_point_t'


class TimerIntgPerstep(models.Model):
    intg_id = models.ForeignKey(TimerIntgPoint)
    perstep_conf = models.TextField()
    perstep_type = models.CharField(max_length=50)  # SELECT\INSERT\UPDATE\DELETE
    created_by = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.CharField(max_length=30)
    last_updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'timer_perstep_t'


class TimerIntgStepRelation(models.Model):
    from_step_id = models.IntegerField()
    to_step_id = models.IntegerField()
    created_by = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.CharField(max_length=30)
    last_updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'timer_step_relation_t'


class TimerIntgFieldMapping(models.Model):
    from_field_id = models.IntegerField(null=True, blank=True)
    from_field_name = models.CharField(max_length=50, null=True, blank=True)
    from_field_nullable = models.CharField(max_length=10, null=True, blank=True)
    to_field_id = models.IntegerField(null=True, blank=True)
    to_field_name = models.CharField(max_length=50, null=True, blank=True)
    to_field_nullable = models.CharField(max_length=10, null=True, blank=True)
    mapping_type = models.CharField(max_length=50)  # mapping\default
    created_by = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.CharField(max_length=30)
    last_updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'timer_field_mapping_t'


class TimerLastRunLog(models.Model):
    job_id = models.CharField(max_length=100)
    task_type = models.CharField(max_length=100)
    task_name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    datacount = models.IntegerField(blank=True, null=True)
    destination = models.CharField(max_length=50, blank=True, null=True)
    message = models.CharField(max_length=400, blank=True, null=True)
    detail = models.TextField(blank=True, null=True)
    created_by = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.CharField(max_length=30)
    last_updated_date = models.DateTimeField(auto_now=True)


class TimerRunLog(models.Model):
    job_id = models.CharField(max_length=100)
    task_type = models.CharField(max_length=100)
    task_name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    datacount = models.IntegerField(blank=True, null=True)
    destination = models.CharField(max_length=50, blank=True, null=True)
    message = models.CharField(max_length=400, blank=True, null=True)
    detail = models.TextField(blank=True, null=True)
    created_by = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.CharField(max_length=30)
    last_updated_date = models.DateTimeField(auto_now=True)


class TimerRunDetail(models.Model):
    job_id = models.CharField(max_length=100)
    task_type = models.CharField(max_length=100)
    task_name = models.CharField(max_length=100)
    operation = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    destination = models.CharField(max_length=50, blank=True, null=True)
    message = models.CharField(max_length=400, blank=True, null=True)
    detail = models.TextField(blank=True, null=True)
    created_by = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.CharField(max_length=30)
    last_updated_date = models.DateTimeField(auto_now=True)


class TimerLastRunLogAdmin(admin.ModelAdmin):
    list_display = ('job_id', 'task_type', 'task_name', 'status', 'destination')


class TimerRunLogAdmin(admin.ModelAdmin):
    list_display = ('job_id', 'task_type', 'task_name', 'status', 'destination')


class TimerRunDetailAdmin(admin.ModelAdmin):
    list_display = ('job_id', 'task_type', 'task_name', 'operation', 'status', 'destination')


admin.site.register(TimerLastRunLog, TimerLastRunLogAdmin)
admin.site.register(TimerRunLog, TimerRunLogAdmin)
admin.site.register(TimerRunDetail, TimerRunDetailAdmin)
