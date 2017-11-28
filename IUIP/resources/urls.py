# -*- coding: utf-8 -*-
from django.conf.urls import url

from resources.views import client_list, loadClientsData, resources_list, loadResourcesData, connectionTest, \
    queryResourceByName

urlpatterns = [
    url(r'^client_list/', client_list),
    url(r'^loadClientsData/', loadClientsData),
    url(r'^resources_list/', resources_list),
    url(r'^loadResourcesData/', loadResourcesData),
    url(r'^connectionTest/', connectionTest),
    url(r'^queryResourceByName/', queryResourceByName),
]