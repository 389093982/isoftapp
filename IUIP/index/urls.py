# -*- coding: utf-8 -*-
from django.conf.urls import url

from index.views import index

urlpatterns = [
    url(r'^index/', index),
]