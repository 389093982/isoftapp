# -*- coding: utf-8 -*-
from django.conf.urls import url

from timer.views import intg_config, intg_dev, intg_list, loadIntgsData, intg_edit, validateSql, getMetaData, \
    saveIntgConfig, intg_del, intg_deploy, intg_stop, intg_start

urlpatterns = [
    url(r'^intg/config/', intg_config),
    url(r'^intg/dev/', intg_dev),
    url(r'^intg/list/', intg_list),
    url(r'^loadIntgsData/', loadIntgsData),
    url(r'^intg/edit/',intg_edit),
    url(r'^validateSql/',validateSql),
    url(r'^validateSql/',validateSql),
    url(r'^getMetaData/',getMetaData),
    url(r'^saveIntgConfig/',saveIntgConfig),
    url(r'^saveIntgConfig/',saveIntgConfig),
    url(r'^intg/del/',intg_del),
    url(r'^intg/deploy/',intg_deploy),
    url(r'^intg/stop/',intg_stop),
    url(r'^intg/start/',intg_start),
]