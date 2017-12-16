# -*- coding: utf-8 -*-

# 解决以下异常引入
# django.core.exceptions.ImproperlyConfigured: Requested setting DEFAULT_INDEX_TABLESPACE, but settings are not configured.
# You must either define the environment variable DJANGO_SETTINGS_MODULE or call settings.configure() before accessing settings.
import json
import os
import time
import uuid

import django
from apscheduler.events import EVENT_JOB_ADDED, EVENT_JOB_REMOVED, EVENT_JOB_MODIFIED, EVENT_JOB_EXECUTED, \
    EVENT_JOB_ERROR, EVENT_JOB_MISSED
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from isoft.common.activemqtool import ActiveMQManager
from isoft.common.singleton import singleton

from IUIP.settings import quartz_apscheduler_job_stroe_url

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IUIP.settings")
django.setup()

import datetime

from quartz.models import ExcludeDispatch, CronMeta


def addExclude(task_type, task_name,
               exclude_from_time=datetime.datetime.strptime("1970-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"),
               exclude_end_time=datetime.datetime.strptime("2100-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")):
    update_or_create_exclude(task_type, task_name, exclude_from_time, exclude_end_time)


def deleteExclude(task_type, task_name):
    update_or_create_exclude(task_type, task_name,
                             exclude_from_time=datetime.datetime.strptime("1970-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"),
                             exclude_end_time=datetime.datetime.strptime("1970-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"))


def update_or_create_exclude(task_type, task_name, exclude_from_time, exclude_end_time):
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ExcludeDispatch.objects.update_or_create(task_type=task_type, task_name=task_name, defaults={
        'exclude_from_time': exclude_from_time,
        'exclude_end_time': exclude_end_time,
        'created_by': 'AutoInsert',
        'created_date': now_time,
        'last_updated_by': 'AutoInsert',
        'last_updated_date': now_time
    })


########################################## quartz_apscheduler_job ####################################################

# 默认30分钟执行一次
def addCronMeta(task_type, task_name, second='*', minute='0,30', hour='*', day='*', month='*',
                day_of_week='*', year='*'):
    CronMeta.objects.create(task_type=task_type, task_name=task_name, second=second, minute=minute, hour=hour, day=day,
                            month=month, day_of_week=day_of_week, year=year)


def deleteCronMeta(task_type, task_name):
    CronMeta.objects.filter(task_type=task_type, task_name=task_name).delete()


LISTENER_JOB = (EVENT_JOB_ADDED |
                EVENT_JOB_REMOVED |
                EVENT_JOB_MODIFIED |
                EVENT_JOB_EXECUTED |
                EVENT_JOB_ERROR |
                EVENT_JOB_MISSED)


def err_listener(events):
    if events.code == EVENT_JOB_MISSED:
        print("Job %s has missed." % str(events.job_id))


jobstores = {
    'sqlalchemy': SQLAlchemyJobStore(url=quartz_apscheduler_job_stroe_url),
    'default': MemoryJobStore()
}
executors = {
    'default': ThreadPoolExecutor(10),
    'processpool': ProcessPoolExecutor(3)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 10
}


def quartz_execute(task_type, task_name):
    try:
        activeMQManager = ActiveMQManager()
        body = json.dumps({'job_id': str(uuid.uuid1()), 'task_type': task_type, 'task_name': task_name})
        destination = '/queue/quartz/scheduler'
        activeMQManager.send(body=body, destination=destination)
    except Exception as e:
        print(str(e))


@singleton
class JobManager(object):
    def __init__(self):
        self.scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults,
                                             timezone='Asia/Shanghai')
        self.jobs = {}
        self.scheduler.add_listener(err_listener, LISTENER_JOB)
        self.scheduler.start()

    def delete_job(self, task_type, task_name):
        if self.scheduler.get_job(job_id=self.get_jobid(task_name, task_type)) is not None:
            self.scheduler.remove_job(job_id=self.get_jobid(task_name, task_type))

    def add_job(self, task_type, task_name, second, minute, hour, day, month, day_of_week, year):
        trigger = dict(second=second, minute=minute, hour=hour, day=day, month=month, day_of_week=day_of_week,
                       year=year)
        Trigger = CronTrigger(**trigger)
        # 生成jobid
        jobid = self.get_jobid(task_type=task_type, task_name=task_name)
        job = self.scheduler.add_job(quartz_execute, Trigger, id=jobid, args=[task_type, task_name])

    def reload_job(self, crons):
        for cron in crons:
            # 添加任务
            self.add_job(cron.task_type, cron.task_name, cron.second,
                         cron.minute, cron.hour, cron.day, cron.month,
                         cron.day_of_week, cron.year)

    def init_jobs(self):
        # crons = CronMeta.objects.all()    # 查询全部
        crons = CronMeta.objects.raw('''
            SELECT
              a.*
            FROM
              quartz_cron_meta_t a
              INNER JOIN exclude_dispatch_t b
                ON a.`task_name` = b.`task_name`
                AND a.`task_type` = b.`task_type`
                AND (
                  b.`exclude_from_time` > SYSDATE()
                  OR b.`exclude_end_time` < SYSDATE()
                )
        ''')
        self.reload_job(crons)

    def get_jobid(self, task_name, task_type):
        # 生成 jobid
        # t = time.time()
        # print(t)                      # 原始时间数据
        # print(int(t))                 # 秒级时间戳
        # print(int(round(t * 1000)))   # 毫秒级时间戳
        return ''.join([task_name, '_', task_type])

