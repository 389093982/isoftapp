# -*- coding: utf-8 -*-
from django.conf.urls import url

from index.views import index, operation_list

urlpatterns = [
    url(r'^index/', index),
    url(r'^operation_list/', operation_list),
]