from django.contrib import admin
from django.db import models

# Create your models here.

class AppId(models.Model):
    app_id = models.CharField(max_length=50)
    app_name = models.CharField(max_length=50)
    app_owner = models.CharField(max_length=30)
    created_by = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.CharField(max_length=30)
    last_updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.app_name

class Projects(models.Model):
    project_name = models.CharField(max_length=50, unique=True)
    app_id = models.ForeignKey(AppId)
    created_by = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.CharField(max_length=30)
    last_updated_date = models.DateTimeField(auto_now=True)

class AppIdAdmin(admin.ModelAdmin):
    fields = ('app_id', 'app_name', 'app_owner', 'created_by', 'last_updated_by')

class ProjectsAdmin(admin.ModelAdmin):
    fields = ('project_id', 'project_name', 'project_appid', 'created_by', 'last_updated_by')

admin.site.register(AppId, AppIdAdmin)
admin.site.register(Projects, ProjectsAdmin)