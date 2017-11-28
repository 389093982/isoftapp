# -*- coding: utf-8 -*-
from django.conf.urls import url

from appmanager.views import edit, loadAppIdsData, loadProjectsData, appid_list, appid_add, projects_list

urlpatterns = [
    url(r'^appid_list/', appid_list),
    url(r'^appid_add/', appid_add),
    url(r'^loadAppIdsData/', loadAppIdsData),
    url(r'^edit/', edit),
    url(r'^projects_list/', projects_list),
    url(r'^loadProjectsData/', loadProjectsData),
]