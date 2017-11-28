from django.contrib import admin
from django.db import models

# Create your models here.

class Environment(models.Model):
    env_name = models.CharField(max_length=50, unique=True)
    created_by = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.CharField(max_length=30)
    last_updated_date = models.DateTimeField(auto_now=True)

class EnvironmentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Environment, EnvironmentAdmin)