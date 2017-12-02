# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models

# Create your models here.

class Dict(models.Model):
    '''数据字典表'''
    dict_query_app = models.CharField(max_length=50)
    dict_query_name = models.CharField(max_length=50)
    dict_key = models.CharField(max_length=50)
    dict_value = models.CharField(max_length=50)
    created_by = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.CharField(max_length=30)
    last_updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Dict: %s, %s, %s, %s' % (self.dict_query_app,self.dict_query_name,self.dict_key,self.dict_value)


class Client(models.Model):
    client_name = models.CharField(max_length=50, unique=True)
    client_short_name = models.CharField(max_length=50, unique=True)
    created_by = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.CharField(max_length=30)
    last_updated_date = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-client_name']         # 分页必须要有默认排序

    def __str__(self):
        return self.client_name

class Resource(models.Model):
    RESOURCE_TYPE_CHOICES = (
        (u'ORACLE', u'ORACLE'),
        (u'MYSQL', u'MYSQL'),
        (u'SQLSERVER', u'SQLSERVER'),
        (u'DB2', u'DB2'),
    )
    resource_name = models.CharField(max_length=50, unique=True)
    resource_type = models.CharField(max_length=50,choices=RESOURCE_TYPE_CHOICES)
    resource_url = models.CharField(max_length=200)
    resource_username = models.CharField(max_length=50)
    resource_password = models.CharField(max_length=50)
    env_name = models.CharField(max_length=50)
    created_by = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.CharField(max_length=30)
    last_updated_date = models.DateTimeField(auto_now=True)
    resource_client = models.ForeignKey(Client)

class ClientAdmin(admin.ModelAdmin):
    pass

class ResourceAdmin(admin.ModelAdmin):
    pass


class DictAdmin(admin.ModelAdmin):
    pass

admin.site.register(Client, ClientAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Dict, DictAdmin)
