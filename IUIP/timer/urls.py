# -*- coding: utf-8 -*-
from django.conf.urls import url

from timer.views import intg_config, intg_dev, intg_list, loadIntgsData, intg_edit, validateSql, getMetaData, \
    intg_del, intg_deploy, intg_stop, intg_start, load_intg_to_engine, log_timer_run_log, \
    log_timer_last_run_log, timer_run_trigger, timer_export

urlpatterns = [
    url(r'^intg/config/', intg_config),
    url(r'^intg/dev/', intg_dev),
    url(r'^intg/list/', intg_list),
    url(r'^loadIntgsData/', loadIntgsData),
    url(r'^intg/edit/',intg_edit),
    url(r'^validateSql/',validateSql),
    url(r'^validateSql/',validateSql),
    url(r'^getMetaData/',getMetaData),
    url(r'^intg/del/',intg_del),
    url(r'^intg/deploy/',intg_deploy),
    url(r'^intg/stop/',intg_stop),
    url(r'^intg/start/',intg_start),
    url(r'^intg/load_intg_to_engine/',load_intg_to_engine),
    url(r'^intg/log_timer_run_log/',log_timer_run_log),
    url(r'^intg/log_timer_last_run_log/',log_timer_last_run_log),
    url(r'^intg/timer_run_trigger/',timer_run_trigger),
    url(r'^intg/export/', timer_export),
]