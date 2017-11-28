# -*- coding: utf-8 -*-

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
