# -*- coding: utf-8 -*-

# Create your views here.
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from quartz.models import SchedulerLog

@csrf_exempt
def add_scheduler_log(request):
    response_data = {}
    response_data['status'] = 'SUCCESS'
    if request.method == "GET":
        try:
            job_id = request.GET.get('job_id')
            task_type = request.GET.get('task_type')
            task_name = request.GET.get('task_name')
            destination = request.GET.get('destination')
            scheduler_log = SchedulerLog()
            scheduler_log.job_id = job_id
            scheduler_log.task_type = task_type
            scheduler_log.task_name = task_name
            scheduler_log.destination = destination
            scheduler_log.created_by = 'quartz'
            scheduler_log.last_updated_by = 'quartz'
            scheduler_log.save()
        except Exception as e:
            response_data['status'] = 'FAILED'
            response_data['error'] = str(e)

    else:
        response_data['status'] = 'FAILED'
        response_data['error'] = '不支持post请求'
    return HttpResponse(json.dumps(response_data))