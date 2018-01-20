# -*- coding: utf-8 -*-

import json
import urllib

from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from isoft.common.dbutil import connection_test
from resources.models import Client, Resource


def updateResourceByClient(request):
    """
    通过系统简称初始化或者修改资源组信息
    operation_title: 操作的标题信息
    operation_url：修改保存按钮的请求地址
    client_short_name：所涉及的系统简称
    resource_name：所涉及的资源组信息,用于回显所用
    :param request:
    :return:
    """
    request.POST = request.GET if request.method == 'GET' else request.POST
    operation_title = urllib.parse.unquote(request.POST.get('operation_title'))
    operation_url = urllib.parse.unquote(request.POST.get('operation_url'))
    client_short_name = urllib.parse.unquote(request.POST.get('client_short_name'))
    resource_name = urllib.parse.unquote(request.POST.get('resource_name'))
    # 获取资源组信息
    resources = Resource.objects.filter(Q(resource_client__client_short_name=client_short_name))
    return render(request, 'resources/updateResourceByClient.html',
                  {'operation_title': operation_title, 'operation_url': operation_url,
                   'client_short_name': client_short_name, 'resource_name': resource_name, 'resources':resources })


def client_list(request):
    return render(request, 'resources/client_list.html')


def loadClientsData(request):
    if request.method == "GET":
        limit = request.GET.get('limit')
        offset = request.GET.get('offset')
        search = request.GET.get('search')
        sort_column = request.GET.get('sortName')
        order = request.GET.get('sortOrder')
        client_name = request.GET.get('client_name')
        client_short_name = request.GET.get('client_short_name')
        if search:
            all_records = Client.objects.filter(Q(client_name__icontains=search)
                                                | Q(client_short_name__icontains=search))
        else:
            all_records = Client.objects.all()

        if sort_column is not None:
            if sort_column in ['client_name', 'client_short_name']:
                if order == 'desc':
                    sort_column = '-%s' % (sort_column)
                all_records = all_records.order_by(sort_column)

        if client_name:
            all_records = all_records.filter(client_name__icontains=client_name)
        if client_short_name:
            all_records = all_records.filter(client_short_name__icontains=client_short_name)
        all_records_count = all_records.count()

        if not offset:
            offset = 0
        if not limit:
            limit = 20
        pageinator = Paginator(all_records, limit)

        page = int(int(offset) / int(limit) + 1)
        response_data = {'total': all_records_count, 'rows': []}
        for client in pageinator.page(page):
            response_data['rows'].append({
                "client_name": client.client_name if client.client_name else "",
                "client_short_name": client.client_short_name if client.client_short_name else "",
                "created_by": client.created_by if client.created_by else "",
                "created_date": client.created_date.strftime('%Y-%m-%d %H:%M') if client.created_date else "",
                "last_updated_by": client.last_updated_by if client.last_updated_by else "",
                "last_updated_date": client.last_updated_date.strftime(
                    '%Y-%m-%d %H:%M') if client.last_updated_date else "",
            })
    return HttpResponse(json.dumps(response_data))


def resources_list(request):
    if request.method == 'GET':
        client_short_name = request.GET.get('client_short_name', '')
        return render(request, 'resources/resources_list.html', {'client_short_name': client_short_name})
    return render(request, 'resources/resources_list.html')


def loadResourcesData(request):
    if request.method == "GET":
        limit = request.GET.get('limit')
        offset = request.GET.get('offset')
        search = request.GET.get('search')
        sort_column = request.GET.get('sortName')
        order = request.GET.get('sortOrder')
        resource_name = request.GET.get('resource_name')
        resource_client = request.GET.get('resource_client')
        if search:
            all_records = Resource.objects.filter(Q(resource_name__icontains=search)
                                                  | Q(resource_client__client_short_name__icontains=search))
        else:
            all_records = Resource.objects.all()
        if sort_column:
            if sort_column in ['resource_name', 'resource_name']:
                if order == 'desc':
                    sort_column = '-%s' % (sort_column)
                all_records = all_records.order_by(sort_column)

        if resource_name:
            all_records = all_records.filter(resource_name__icontains=resource_name)
        if resource_client:
            all_records = all_records.filter(resource_client__client_short_name__icontains=resource_client)
        all_records_count = all_records.count()

        if not offset:
            offset = 0
        if not limit:
            limit = 20
        pageinator = Paginator(all_records, limit)

        page = int(int(offset) / int(limit) + 1)
        response_data = {'total': all_records_count, 'rows': []}

        index = 0
        for resource in pageinator.page(page):
            response_data['rows'].append({
                "id": index,  # 设置索引
                "resource_name": resource.resource_name if resource.resource_name else "",
                "resource_type": resource.resource_type if resource.resource_type else "",
                "resource_url": resource.resource_url if resource.resource_url else "",
                "resource_username": resource.resource_username if resource.resource_username else "",
                "resource_password": resource.resource_password if resource.resource_password else "",
                "env_name": resource.env_name if resource.env_name else "",
                "client_short_name": resource.resource_client.client_short_name if resource.resource_client.client_short_name else "",
                "connection_test": "待测试",
            })
            index = index + 1
    return HttpResponse(json.dumps(response_data))


@csrf_exempt
def connectionTest(request):
    if request.method == "POST":
        url = request.POST.get('url')
        username = request.POST.get('username')
        password = request.POST.get('password')
        dbType = request.POST.get('dbType')

        # d = {'url':url, 'username':username, 'password':password, 'dbType':dbType}
        try:
            # r = requests.post('http://127.0.0.1:8080/resources/connectionTest', data=d)
            connection_test(url, username, password, dbType)
        except Exception as e:
            return HttpResponse(json.dumps({'status': 'ERROR', 'result': str(e)}), content_type="application/json")
        return HttpResponse(json.dumps({'status': 'SUCCESS', 'result': 'SUCCESS'}), content_type="application/json")


@csrf_exempt
def queryResourceByName(request):
    response_data = {}
    try:
        resourceName = request.POST.get("resourceName")
        resources = Resource.objects.filter(resource_name=resourceName)
        response_data['status'] = 'success'
        # model_to_dict 进行转换
        response_data['resource'] = model_to_dict(resources[0])
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    except Exception as e:
        response_data['status'] = 'error'
        response_data['errorMsg'] = str(e)
        return HttpResponse(json.dumps(response_data), content_type="application/json")
