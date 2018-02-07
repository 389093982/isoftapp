# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm

from appmanager.models import AppId, Projects


class AppIdForm(ModelForm):
    class Meta:
        model = AppId
        fields = ('app_id','app_name','app_owner','created_by')

    app_id = forms.CharField(error_messages={'required':u'app_id 不能为空'})
    app_name = forms.CharField(error_messages={'required':u'app_name 不能为空'})
    app_owner = forms.CharField(error_messages={'required':u'app_owner 不能为空'})
    created_by = forms.CharField(error_messages={'required':u'created_by 不能为空'})

    def clean(self):
        cleaned_data = super(AppIdForm,self).clean()
        app_id_data = cleaned_data.get('app_id')
        app_name_data = cleaned_data.get('app_name')

        if app_id_data.strip() != app_name_data.strip():
            msg = u'app_id 必须与 app_name 保持一致!'
            self._errors['app_id'] = self.error_class([msg])
            del cleaned_data['app_id']
            msg = u'app_name 必须与 app_id 保持一致!'
            self._errors['app_name'] = self.error_class([msg])
            del cleaned_data['app_name']
        return cleaned_data

class ProjectForm(ModelForm):
    class Meta:
        model = Projects
        fields = ('project_name','created_by','last_updated_by')

    def __init__(self,*args,**kwargs):
        super(ProjectForm,self).__init__(*args,**kwargs)
        self.fields['app_id'].choices= ((x.id,x.app_name) for x in AppId.objects.all())

    app_id = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), label='应用名称')
    project_name = forms.CharField(error_messages={'required':u'project_name 不能为空'}, label='项目名称')
    created_by = forms.CharField(error_messages={'required':u'created_by 不能为空'}, label='创建人员')
    last_updated_by = forms.CharField(error_messages={'required':u'last_updated_by 不能为空'}, label='修改人员')

    def clean(self):
        cleaned_data = super(ProjectForm, self).clean()
        project_name = cleaned_data.get('project_name')
        if Projects.objects.filter(project_name=project_name).first():
            msg = u'project_name 已存在,请选择其它名称进行注册!'
            self._errors['project_name'] = self.error_class([msg])
            del cleaned_data['project_name']
        return cleaned_data