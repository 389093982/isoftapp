# -*- coding: utf-8 -*-
import json
import urllib

from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index/index_.html')


def operation_list(request):
    '''
    显示操作清单通用视图函数
    需要传入以下参数
    backup_url: 返回按钮的url地址
    operation_title：显示的标题
    operations：具体的操作清单,格式如下,是个字符串,使用json.load进行转换然后渲染模板
    [{'operation_name':'operation_name','operation_url':'operation_url','operatable': 'true'},
                  {'operation_name': 'operation_name', 'operation_url': 'operation_url','operatable': 'false'}]
    '''
    request.POST = request.GET if request.method == 'GET' else request.POST
    backup_url = urllib.parse.unquote(request.POST.get('backup_url',None))
    operation_title = urllib.parse.unquote(request.POST.get('operation_title',None))
    operations = urllib.parse.unquote(request.POST.get('operations',None))
    return render(request, 'index/operation_list.html',
                  {'backup_url':backup_url,'operation_title':operation_title,'operations':json.loads(operations)})

