# -*- coding: utf-8 -*-
from django.conf.urls import url

from appmanager.views import loadAppIdsData, loadProjectsData, appid_list, projects_list, appid_edit, appid_delete, \
    projects_add, project_delete

urlpatterns = [
    url(r'^appid_list/', appid_list),
    url(r'^loadAppIdsData/', loadAppIdsData),
    url(r'^appid_edit/', appid_edit),
    url(r'^appid_delete/', appid_delete),
    url(r'^projects_list/', projects_list),
    url(r'^loadProjectsData/', loadProjectsData),
    url(r'^projects_add/', projects_add),
    url(r'^project_delete/', project_delete),
]