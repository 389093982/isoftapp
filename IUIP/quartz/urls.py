# -*- coding: utf-8 -*-
from django.conf.urls import url

from quartz.views import add_scheduler_log

urlpatterns = [
    url(r'^scheduler/log/add/', add_scheduler_log),
]