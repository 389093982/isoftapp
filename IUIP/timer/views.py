# -*- coding: utf-8 -*-

import json
from datetime import date, datetime

from django.core import serializers
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from isoft.common import dbutil
from quartz.core.scheduler import deleteExclude, addCronMeta, deleteCronMeta, JobManager, addExclude
from quartz.models import CronMeta
from resources.models import Resource
from timer.forms import IntgConfigForm
from timer.models import IntgList, TimerIntgPoint, TimerIntgPerstep, TimerIntgFieldMapping, TimerIntgStepRelation, \
    TimerRunDetail, TimerLastRunLog, TimerRunLog


@csrf_exempt
def log_timer_last_run_log(request):
    response_data = {}
    if request.method == 'GET':
        try:
            job_id = request.GET.get('job_id')
            task_type = request.GET.get('task_type')
            task_name = request.GET.get('task_name')
            status = request.GET.get('status')
            datacount = request.GET.get('datacount')
            destination = request.GET.get('destination')
            message = request.GET.get('message')
            detail = request.GET.get('detail')
            created_by = request.GET.get('created_by')
            last_updated_by = request.GET.get('last_updated_by')

            TimerLastRunLog.objects.update_or_create(task_type=task_type, task_name=task_name,
                                                     defaults={
                                                         'job_id': job_id, 'task_type': task_type,
                                                         'task_name': task_name, 'status': status,
                                                         'datacount': datacount,
                                                         'destination': destination, 'message': message,
                                                         'detail': detail,
                                                         'created_by': created_by, 'last_updated_by': last_updated_by
                                                     })
            TimerRunLog.objects.create(job_id=job_id, task_type=task_type, task_name=task_name,
                                       status=status, datacount=datacount, destination=destination,
                                       message=message, detail=detail, created_by=created_by,
                                       last_updated_by=last_updated_by)
        except Exception as e:
            print(str(e))
    else:
        response_data['status'] = 'ERROR'
        response_data['errorMsg'] = 'unsupoort request method: %s' % request.method
    return HttpResponse(json.dumps(response_data, ensure_ascii=False, cls=DateEncoder), content_type="application/json")


@csrf_exempt
def log_timer_run_log(request):
    response_data = {}
    if request.method == 'GET':
        try:
            job_id = request.GET.get('job_id')
            task_type = request.GET.get('task_type')
            task_name = request.GET.get('task_name')
            operation = request.GET.get('operation')
            status = request.GET.get('status')
            destination = request.GET.get('destination')
            message = request.GET.get('message')
            detail = request.GET.get('detail')
            created_by = request.GET.get('created_by')
            last_updated_by = request.GET.get('last_updated_by')

            timerRunDetail = TimerRunDetail()
            timerRunDetail.job_id = job_id
            timerRunDetail.task_type = task_type
            timerRunDetail.task_name = task_name
            timerRunDetail.operation = operation
            timerRunDetail.status = status
            timerRunDetail.destination = destination
            timerRunDetail.message = message
            timerRunDetail.detail = detail
            timerRunDetail.created_by = created_by
            timerRunDetail.last_updated_by = last_updated_by

            timerRunDetail.save()
        except Exception as e:
            print(str(e))
    else:
        response_data['status'] = 'ERROR'
        response_data['errorMsg'] = 'unsupoort request method: %s' % request.method
    return HttpResponse(json.dumps(response_data, ensure_ascii=False, cls=DateEncoder), content_type="application/json")


@csrf_exempt
def load_intg_to_engine(request):
    '''往引擎中加载集成点'''
    response_data = {}
    intg_data = {}
    if request.method == 'GET':
        try:
            task_type = request.GET['task_type']
            task_name = request.GET['task_name']
            if task_type == 'Timer':
                # 查询 TimerIntgPoint 表数据
                timerIntgPoint = TimerIntgPoint.objects.filter(integration_point_name=task_name[0:task_name.rfind('_')],
                                                               integration_point_version=task_name[task_name.rfind(
                                                                   '_') + 1:]).first()
                intg_data['timerIntgPoint'] = serializers.serialize('json', [timerIntgPoint])
                # 查询 TimerIntgPerstep 表数据
                timerIntgPersteps = TimerIntgPerstep.objects.filter(intg_id=timerIntgPoint.id)
                intg_data['timerIntgPersteps'] = serializers.serialize('json', timerIntgPersteps)
                # 查询 TimerIntgStepRelation 表数据
                timerIntgStepRelations = TimerIntgStepRelation.objects.filter(
                    Q(from_step_id__in=timerIntgPersteps.values('id'))
                    | Q(to_step_id__in=timerIntgPersteps.values('id')))
                intg_data['timerIntgStepRelations'] = serializers.serialize('json', timerIntgStepRelations)
                # 查询 TimerIntgFieldMapping 表数据
                timerIntgFieldMappings = TimerIntgFieldMapping.objects.filter(
                    Q(from_field_id__in=timerIntgPersteps.values('id'))
                    | Q(to_field_id__in=timerIntgPersteps.values('id')))
                intg_data['timerIntgFieldMappings'] = serializers.serialize('json', timerIntgFieldMappings)
                # 查询资源组信息
                source_db_conn = Resource.objects.filter(resource_name=timerIntgPoint.source_db_conn)
                target_db_conn = Resource.objects.filter(resource_name=timerIntgPoint.target_db_conn)
                intg_data['source_db_conn'] = serializers.serialize('json', source_db_conn)
                intg_data['target_db_conn'] = serializers.serialize('json', target_db_conn)
                response_data['status'] = 'SUCCESS'
                response_data['intg_data'] = intg_data
            else:
                response_data['status'] = 'ERROR'
                response_data['errorMsg'] = 'unsupport task_type: %s' % task_type
        except Exception as e:
            response_data['status'] = 'ERROR'
            response_data['errorMsg'] = str(e)
    else:
        response_data['status'] = 'ERROR'
        response_data['errorMsg'] = 'unsupoort request method: %s' % request.method
    return HttpResponse(json.dumps(response_data, ensure_ascii=False, cls=DateEncoder), content_type="application/json")


def update_intg_status(integration_point_name, integration_point_version, status):
    # 更新集成点状态
    TimerIntgPoint.objects.filter(integration_point_name=integration_point_name,
                                  integration_point_version=integration_point_version).update(
        integration_point_status=status)
    IntgList.objects.filter(integration_point_name=integration_point_name,
                            integration_point_version=integration_point_version).update(status=status)


def intg_start(request):
    if request.method == 'GET':
        try:
            integration_point_name = request.GET['integration_point_name']
            integration_point_version = request.GET['integration_point_version']
            task_type = 'Timer'
            task_name = ''.join([integration_point_name, '_', integration_point_version])
            # 更新集成点状态
            update_intg_status(integration_point_name=integration_point_name,
                               integration_point_version=integration_point_version, status=2)
            # 添加不可调度
            deleteExclude(task_type=task_type, task_name=task_name)
            # 添加/更新任务
            job_manager = JobManager()
            task_type = 'Timer'
            task_name = ''.join([integration_point_name, '_', integration_point_version])
            crons = CronMeta.objects.filter(task_type=task_type, task_name=task_name)
            job_manager.reload_job(crons)
            return HttpResponse(json.dumps({'status': 'SUCCESS', 'result': 'SUCCESS'}))
        except Exception as e:
            return HttpResponse(json.dumps({'status': 'ERROR', 'result': 'deploy failed:' + str(e)}))


def intg_stop(request):
    if request.method == 'GET':
        try:
            integration_point_name = request.GET['integration_point_name']
            integration_point_version = request.GET['integration_point_version']
            task_type = 'Timer'
            task_name = ''.join([integration_point_name, '_', integration_point_version])
            # 更新集成点状态
            update_intg_status(integration_point_name=integration_point_name,
                               integration_point_version=integration_point_version, status=3)
            # 添加不可调度
            addExclude(task_type=task_type, task_name=task_name)
            # 添加/更新任务
            job_manager = JobManager()
            job_manager.delete_job(task_type=task_type, task_name=task_name)
            return HttpResponse(json.dumps({'status': 'SUCCESS', 'result': 'SUCCESS'}))
        except Exception as e:
            return HttpResponse(json.dumps({'status': 'ERROR', 'result': 'deploy failed:' + str(e)}))


def intg_deploy(request):
    if request.method == 'GET':
        try:
            integration_point_name = request.GET['integration_point_name']
            integration_point_version = request.GET['integration_point_version']
            task_type = 'Timer'
            task_name = ''.join([integration_point_name, '_', integration_point_version])
            # 删除不可调度
            deleteExclude(task_type=task_type, task_name=task_name)
            # 添加默认频率
            deleteCronMeta(task_type=task_type, task_name=task_name)
            addCronMeta(task_type=task_type, task_name=task_name)
            # 添加/更新任务
            job_manager = JobManager()
            # 1、先删除任务
            job_manager.delete_job(task_type=task_type, task_name=task_name)
            # 2、再添加任务
            crons = CronMeta.objects.filter(task_type=task_type, task_name=task_name)
            for cron in crons:
                job_manager.add_job(task_type=task_type, task_name=task_name, second=cron.second, minute=cron.minute,
                                    hour=cron.hour, day=cron.day, month=cron.month, day_of_week=cron.day_of_week,
                                    year=cron.year)
            # 更新集成点状态
            TimerIntgPoint.objects.filter(integration_point_name=integration_point_name,
                                          integration_point_version=integration_point_version).update(
                integration_point_status=2)
            IntgList.objects.filter(integration_point_name=integration_point_name,
                                    integration_point_version=integration_point_version).update(
                status=2)
            return HttpResponse(json.dumps({'status': 'SUCCESS', 'result': 'SUCCESS'}))
        except Exception as e:
            return HttpResponse(json.dumps({'status': 'ERROR', 'result': 'deploy failed:' + str(e)}))


@csrf_exempt
def intg_del(request):
    if request.method == 'GET':
        try:
            integration_point_name = request.GET['integration_point_name']
            integration_point_version = request.GET['integration_point_version']
            # 删除 List 表
            IntgList.objects.filter(integration_point_name=integration_point_name,
                                    integration_point_version=integration_point_version).delete()
            # 删除 Timer 四张表

            timerIntgPoint = TimerIntgPoint.objects.filter(integration_point_name=integration_point_name,
                                                           integration_point_version=integration_point_version).first()
            if timerIntgPoint is not None:
                timerIntgPersteps = TimerIntgPerstep.objects.filter(intg_id=timerIntgPoint.id)
                timerIntgStepRelations = TimerIntgStepRelation.objects.filter(
                    Q(from_step_id__in=timerIntgPersteps.values('id'))
                    | Q(to_step_id__in=timerIntgPersteps.values('id')))
                timerIntgFieldMappings = TimerIntgFieldMapping.objects.filter(
                    Q(from_field_id__in=timerIntgPersteps.values('id'))
                    | Q(to_field_id__in=timerIntgPersteps.values('id')))
                timerIntgFieldMappings.delete()
                timerIntgStepRelations.delete()
                timerIntgPersteps.delete()
                timerIntgPoint.delete()
            return HttpResponse(json.dumps({'status': 'SUCCESS', 'result': 'SUCCESS'}))
        except Exception as e:
            return HttpResponse(json.dumps({'status': 'ERROR', 'result': 'delete failed:' + str(e)}))


@csrf_exempt
def saveIntgConfig(request):
    if request.method == "POST":
        source_client_name = request.POST.get('source_client_name')
        target_client_name = request.POST.get('target_client_name')
        integration_point_name = request.POST.get('integration_point_name')
        integration_point_version = request.POST.get('integration_point_version')
        src_resource_name = request.POST.get('src_resource_name')
        target_resource_name = request.POST.get('target_resource_name')
        sqlArray = request.POST.get('sqlArray')
        fieldMappingArray = request.POST.get('fieldMappingArray')

        timerIntgPoint = TimerIntgPoint()
        timerIntgPoint.integration_point_name = integration_point_name
        timerIntgPoint.integration_point_version = integration_point_version
        timerIntgPoint.env_name = 'default'
        timerIntgPoint.integration_point_status = 1
        timerIntgPoint.source_db_conn = src_resource_name
        timerIntgPoint.target_db_conn = target_resource_name
        timerIntgPoint.source_client_name = source_client_name
        timerIntgPoint.target_client_name = target_client_name
        timerIntgPoint.created_by = 'AutoInsert'
        timerIntgPoint.last_updated_by = 'AutoInsert'
        timerIntgPoint.created_date = None
        timerIntgPoint.last_updated_date = None
        timerIntgPoint.save()

        sqlArrayObj = json.loads(sqlArray)
        fieldMappingArrayObj = json.loads(fieldMappingArray)

        for index, sqlMappingObj in enumerate(sqlArrayObj):
            src_sql = sqlMappingObj[0]
            target_sql = sqlMappingObj[1]
            src_timerIntgPerstep = TimerIntgPerstep()
            src_timerIntgPerstep.intg_id = timerIntgPoint
            src_timerIntgPerstep.perstep_conf = src_sql
            src_timerIntgPerstep.perstep_type = 'SELECT'
            src_timerIntgPerstep.perstep_attribute = 'SOURCE'
            src_timerIntgPerstep.created_by = 'AutoInsert'
            src_timerIntgPerstep.last_updated_by = 'AutoInsert'
            src_timerIntgPerstep.created_date = None
            src_timerIntgPerstep.last_updated_date = None
            src_timerIntgPerstep.save()

            target_timerIntgPerstep = TimerIntgPerstep()
            target_timerIntgPerstep.intg_id = timerIntgPoint
            target_timerIntgPerstep.perstep_conf = target_sql
            target_timerIntgPerstep.perstep_type = 'INSERT'
            target_timerIntgPerstep.perstep_attribute = 'TARGET'
            target_timerIntgPerstep.created_by = 'AutoInsert'
            target_timerIntgPerstep.last_updated_by = 'AutoInsert'
            target_timerIntgPerstep.created_date = None
            target_timerIntgPerstep.last_updated_date = None
            target_timerIntgPerstep.save()

            timerIntgStepRelation = TimerIntgStepRelation()
            timerIntgStepRelation.from_step_id = src_timerIntgPerstep.id
            timerIntgStepRelation.to_step_id = target_timerIntgPerstep.id
            timerIntgStepRelation.created_by = 'AutoInsert'
            timerIntgStepRelation.last_updated_by = 'AutoInsert'
            timerIntgStepRelation.created_date = None
            timerIntgStepRelation.last_updated_date = None
            timerIntgStepRelation.save()

            fieldMappingObj = fieldMappingArrayObj[index]
            src_fieldMappingObj = fieldMappingObj[0]
            target_fieldMappingObj = fieldMappingObj[0]

            maxRows = 0
            if len(src_fieldMappingObj) > len(target_fieldMappingObj):
                maxRows = len(src_fieldMappingObj)
            else:
                maxRows = len(target_fieldMappingObj)
            for i in range(maxRows):
                timerIntgFieldMapping = TimerIntgFieldMapping()
                if i < len(src_fieldMappingObj):
                    timerIntgFieldMapping.from_field_id = src_timerIntgPerstep.id
                    timerIntgFieldMapping.from_field_name = src_fieldMappingObj[i][0]
                    timerIntgFieldMapping.from_field_type = None
                    timerIntgFieldMapping.from_field_length = None
                    timerIntgFieldMapping.from_field_nullable = src_fieldMappingObj[i][6]
                if i < len(target_fieldMappingObj):
                    timerIntgFieldMapping.to_field_id = target_timerIntgPerstep.id
                    timerIntgFieldMapping.to_field_name = target_fieldMappingObj[i][0]
                    timerIntgFieldMapping.to_field_type = None
                    timerIntgFieldMapping.to_field_length = None
                    timerIntgFieldMapping.to_field_nullable = target_fieldMappingObj[i][6]
                timerIntgFieldMapping.created_by = 'AutoInsert'
                timerIntgFieldMapping.last_updated_by = 'AutoInsert'
                timerIntgFieldMapping.created_date = None
                timerIntgFieldMapping.last_updated_date = None
                timerIntgFieldMapping.save()

        IntgList.objects.filter(integration_point_name=integration_point_name,
                                integration_point_version=integration_point_version).update(status=1)
        return HttpResponse(json.dumps({'status': 'SUCCESS', 'result': 'SUCCESS'}))


@csrf_exempt
def getMetaData(request):
    if request.method == "POST":
        src_sql = request.POST.get('src_sql')
        src_resource_type = request.POST.get('src_resource_type')
        src_resource_url = request.POST.get('src_resource_url')
        src_resource_username = request.POST.get('src_resource_username')
        src_resource_password = request.POST.get('src_resource_password')
        target_sql = request.POST.get('target_sql')
        target_resource_type = request.POST.get('target_resource_type')
        target_resource_url = request.POST.get('target_resource_url')
        target_resource_username = request.POST.get('target_resource_username')
        target_resource_password = request.POST.get('target_resource_password')

        try:
            src_meta = dbutil.getMetaData(src_resource_type, src_resource_url, src_resource_username,
                                          src_resource_password,
                                          src_sql)
            target_meta = dbutil.getMetaData(target_resource_type, target_resource_url, target_resource_username,
                                             target_resource_password, target_sql)

            return HttpResponse(json.dumps({'status': 'SUCCESS', 'src_meta': src_meta, 'target_meta': target_meta}),
                                content_type="application/json")
        except Exception as e:
            return HttpResponse(json.dumps({'status': 'ERROR', 'result': str(e)}), content_type="application/json")


@csrf_exempt
def validateSql(request):
    if request.method == "POST":
        resource_type = request.POST.get('resource_type')
        resource_url = request.POST.get('resource_url')
        resource_username = request.POST.get('resource_username')
        resource_password = request.POST.get('resource_password')
        sql = request.POST.get('sql')

        try:
            dbutil.validateSql(resource_type, resource_url, resource_username, resource_password, sql)
        except Exception as e:
            return HttpResponse(json.dumps({'status': 'ERROR', 'result': str(e)}), content_type="application/json")
        return HttpResponse(json.dumps({'status': 'SUCCESS', 'result': 'SUCCESS'}), content_type="application/json")


def intg_edit(request):
    integration_point_name = request.GET['integration_point_name']
    integration_point_version = request.GET['integration_point_version']
    # 截取获取源宿系统
    client_name = integration_point_name[0:integration_point_name.index('(')]
    source_client_name = client_name[0:client_name.index('2')]
    target_client_name = client_name[client_name.index('2') + 1:]
    # 获取源宿资源组
    src_resources = Resource.objects.filter(Q(resource_client__client_short_name=source_client_name))
    target_resources = Resource.objects.filter(Q(resource_client__client_short_name=target_client_name))

    timerIntgPoint = TimerIntgPoint.objects.filter(integration_point_name=integration_point_name,
                                                   integration_point_version=integration_point_version).first()
    timerIntgPersteps = None
    timerIntgStepRelations = None
    if timerIntgPoint is not None:
        timerIntgPersteps = TimerIntgPerstep.objects.filter(intg_id=timerIntgPoint.id)
        timerIntgStepRelations = TimerIntgStepRelation.objects.filter(
            Q(from_step_id__in=timerIntgPersteps.values('id'))
            | Q(to_step_id__in=timerIntgPersteps.values('id')))
    return render(request, 'timer/intg_edit.html',
                  {'integration_point_name': integration_point_name,
                   'integration_point_version': integration_point_version,
                   'src_resources': src_resources, 'target_resources': target_resources,
                   'source_client_name': source_client_name, 'target_client_name': target_client_name,
                   'timerIntgPoint': timerIntgPoint, 'timerIntgPersteps': timerIntgPersteps,
                   'timerIntgStepRelations': timerIntgStepRelations})


def intg_config(request):
    if request.method == 'POST':
        form = IntgConfigForm(request.POST)
        if form.is_valid():
            # 获取表单信息
            source_client_name = form.cleaned_data['source_client_name']
            target_client_name = form.cleaned_data['target_client_name']
            target_table_name = form.cleaned_data['target_table_name']
            business_meaning = form.cleaned_data['business_meaning']
            description = form.cleaned_data['description']
            initial_deploy_env = form.cleaned_data['initial_deploy_env']

            integration_point_name = ''.join(
                [source_client_name, '2', target_client_name, '(', target_table_name, ')_', business_meaning, '_Timer'])
            intg_list = IntgList(integration_point_name=integration_point_name, integration_point_version='v1.0',
                                 env_name=initial_deploy_env, status=0, source_client_name=source_client_name,
                                 target_client_name=target_client_name, created_by='SYSTEM', last_updated_by='SYSTEM')
            intg_list.save()
            return HttpResponseRedirect('/timer/intg/list/')
    else:
        form = IntgConfigForm()
    return render(request, 'timer/intg_config.html', {'form': form})


def intg_dev(request):
    return HttpResponse('helloworld')


# 集成清单
def intg_list(request):
    return render(request, 'timer/intg_list.html')


def loadIntgsData(request):
    if request.method == "GET":
        limit = request.GET.get('limit')
        offset = request.GET.get('offset')
        search = request.GET.get('search')
        sort_column = request.GET.get('sortName')
        order = request.GET.get('sortOrder')
        integration_point_name = request.GET.get('integration_point_name')
        env_name = request.GET.get('env_name')
        source_client_name = request.GET.get('source_client_name')
        target_client_name = request.GET.get('target_client_name')
        if search:
            all_records = IntgList.objects.filter(Q(integration_point_name__icontains=search)
                                                  | Q(env_name__icontains=search)
                                                  | Q(source_client_name__icontains=search)
                                                  | Q(target_client_name__icontains=search))
        else:
            all_records = IntgList.objects.all()
        if sort_column:
            if sort_column in ['integration_point_name', 'env_name', 'source_client_name', 'target_client_name']:
                if order == 'desc':
                    sort_column = '-%s' % (sort_column)
                all_records = all_records.order_by(sort_column)

        if integration_point_name:
            all_records = all_records.filter(integration_point_name__icontains=integration_point_name)
        if env_name:
            all_records = all_records.filter(env_name__icontains=env_name)
        if source_client_name:
            all_records = all_records.filter(source_client_name__icontains=source_client_name)
        if target_client_name:
            all_records = all_records.filter(target_client_name__icontains=target_client_name)
        all_records = all_records.order_by('-last_updated_date')
        all_records_count = all_records.count()

        if not offset:
            offset = 0
        if not limit:
            limit = 20
        pageinator = Paginator(all_records, limit)

        page = int(int(offset) / int(limit) + 1)
        response_data = {'total': all_records_count, 'rows': []}

        index = 0
        for intg in pageinator.page(page):
            response_data['rows'].append({
                "id": index,  # 设置索引
                "integration_point_name": intg.integration_point_name if intg.integration_point_name else "",
                "integration_point_version": intg.integration_point_version if intg.integration_point_version else "",
                "env_name": intg.env_name if intg.env_name else "",
                "status": intg.status if intg.status else 0,
                "source_client_name": intg.source_client_name if intg.source_client_name else "",
                "target_client_name": intg.target_client_name if intg.target_client_name else "",
                "last_updated_date": intg.last_updated_date if intg.last_updated_date else "",
            })
            index = index + 1
    return HttpResponse(json.dumps(response_data, cls=DateEncoder))


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)
