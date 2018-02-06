import json

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from appmanager.forms import AppIdForm
from appmanager.models import AppId, Projects

@csrf_exempt
def loadProjectsData(request):
    if request.method == "POST":
        limit = request.POST.get('limit')
        offset = request.POST.get('offset')
        search = request.POST.get('search')
        sort_column = request.POST.get('sortName')
        order = request.POST.get('sortOrder')
        project_id = request.POST.get('project_id')
        project_name = request.POST.get('project_name')
        project_appid = request.POST.get('project_appid')
        if search:
            all_records = Projects.objects.filter(Q(project_id__icontains=search)
                                               | Q(project_name__icontains=search) | Q(project_appid__app_name__icontains=search))
        else:
            all_records = Projects.objects.all()
        if sort_column:
            if sort_column in ['project_id', 'project_name', 'project_appid']:
                if order == 'desc':
                    sort_column = '-%s' % (sort_column)
                all_records = all_records.order_by(sort_column)

        if project_id:
            all_records = all_records.filter(project_id__icontains=project_id)
        if project_name:
            all_records = all_records.filter(project_name__icontains=project_name)
        if project_appid:
            # 方法一、首先获得外键指向的表中对象，然后通过'_set'这样的方法获得目标表中的数据
            # obj = AppId.objects.get(app_id = project_appid)
            # all_records = obj.projects_set.all()
            # 方法二、直接在目标表中通过双下划线来指定外键对应表中的域来查找符合条件的对象
            all_records = all_records.filter(project_appid__app_id__icontains=project_appid)

        all_records_count = all_records.count()

        if not offset:
            offset = 0
        if not limit:
            limit = 20
        pageinator = Paginator(all_records, limit)

        page = int(int(offset) / int(limit) + 1)
        response_data = {'total': all_records_count, 'rows': []}
        for project in pageinator.page(page):
            response_data['rows'].append({
                "project_id": project.project_id if project.project_id else "",
                "project_name": project.project_name if project.project_name else "",
                "project_appid": project.project_appid.app_id if project.project_appid.app_id else "",
                "created_by": project.created_by if project.created_by else "",
                "created_date": project.created_date.strftime('%Y-%m-%d %H:%M') if project.created_date else "",
                "last_updated_by": project.last_updated_by if project.last_updated_by else "",
                "last_updated_date": project.last_updated_date.strftime('%Y-%m-%d %H:%M') if project.last_updated_date else "",
            })
    return HttpResponse(json.dumps(response_data))

def projects_list(request):
    if request.method == 'GET':
        app_id = request.GET.get('app_id','')
        return render(request,'appmanager/projects_list.html',{'app_id': app_id })
    return render(request, 'appmanager/projects_list.html')

def appid_delete(request):
    request.POST = request.POST if request.POST else request.GET
    response_data = {}
    try:
        app_id = request.POST.get('app_id')
        AppId.objects.filter(app_id=app_id).delete()
        response_data['status'] = 'SUCCESS'
        response_data['msg'] = '删除成功!'
    except Exception as e:
        response_data['status'] = 'ERROR'
        response_data['msg'] = '删除失败!'
    return HttpResponse(json.dumps(response_data))

@csrf_exempt
def loadAppIdsData(request):
    if request.method == "POST":
        page = request.POST.get('page')
        rows = request.POST.get('rows')
        sort = request.POST.get('sort')
        order = request.POST.get('order')
        app_id = request.POST.get('app_id')
        app_name = request.POST.get('app_name')
        app_owner = request.POST.get('app_owner')
        all_records = AppId.objects.all()   # must be wirte the line code here

        if sort:                         # 判断是否有排序需求
            if sort in ['app_id', 'app_name', 'app_owner']:  # 如果排序的列表在这些内容里面
                if order == 'desc':             # 如果排序是反向
                    sort = '-%s' % (sort)
                all_records = all_records.order_by(sort)

        if app_id:
            all_records = all_records.filter(app_id__icontains=app_id)
        if app_name:
            all_records = all_records.filter(app_name__icontains=app_name)
        if app_owner:
            all_records = all_records.filter(app_owner__icontains=app_owner)

        all_records_count = all_records.count()

        page = int(page) if page is not None else 1
        rows = int(rows) if rows is not None else 10
        pageinator = Paginator(all_records, rows)  # 开始做分页

        # 必须带有rows和total这2个key，total表示总页数，rows表示每行的内容
        response_data = {'total': all_records_count, 'rows': []}
        for appId in pageinator.page(page):
            response_data['rows'].append({
                "app_id": appId.app_id if appId.app_id else "",
                "app_name": appId.app_name if appId.app_name else "",
                "app_owner": appId.app_owner if appId.app_owner else "",
                "created_by": appId.created_by if appId.created_by else "",
                "created_date": appId.created_date.strftime('%Y-%m-%d %H:%M') if appId.created_date else "",
                "last_updated_by": appId.last_updated_by if appId.last_updated_by else "",
                "last_updated_date": appId.last_updated_date.strftime('%Y-%m-%d %H:%M') if appId.last_updated_date else "",
            })
        return HttpResponse(json.dumps(response_data))      # 需要json处理下数据格式

def appid_list(request):
    return render(request,'appmanager/appid_list.html')

def appid_edit(request):
    '''
        get 请求：
            无 app_id 表示新增
            有 app_id 表示修改
        post 请求：
            无 edit 标识表示提交
            有 edit 标识表示更新
    '''
    if request.method == 'GET':
        app_id = request.GET.get('app_id')
        if app_id:
            obj = AppId.objects.filter(app_id=app_id).first()
            form = AppIdForm(instance=obj)
            return render(request, 'appmanager/appid_edit.html', {'form': form, 'edit': 'edit'})
        else:
            form = AppIdForm()
            return render(request, 'appmanager/appid_edit.html', {'form': form})
    else:
        if request.POST.get('submit') == 'cancel':
            return HttpResponseRedirect('/appmanager/appid_list/')
        else:
            form = AppIdForm(request.POST)
            if form.is_valid():
                # 获取表单信息
                app_id = form.cleaned_data['app_id']
                app_name = form.cleaned_data['app_name']
                app_owner = form.cleaned_data['app_owner']
                created_by = form.cleaned_data['created_by']
                # 将表单写入数据库
                AppId.objects.update_or_create(app_id=app_id, app_name=app_name, defaults={
                    'app_owner': app_owner, 'created_by': created_by, 'last_updated_by': created_by
                })
                return HttpResponseRedirect('/appmanager/appid_list/')
            else:
                if request.POST.get('edit'):
                    return render(request, 'appmanager/appid_edit.html', {'form': form, 'edit': 'edit'})
                else:
                    return render(request, 'appmanager/appid_edit.html', {'form': form})

