# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm

from appmanager.models import AppId


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
        if AppId.objects.filter(app_id=app_id_data).count() is not 0:
            msg = u'app_id已经存在!'
            self._errors['app_id'] = self.error_class([msg])
            del cleaned_data['app_id']
        if AppId.objects.filter(app_name=app_name_data).count() is not 0:
            msg = u'app_name已经存在!'
            self._errors['app_name'] = self.error_class([msg])
            del cleaned_data['app_name']
        return cleaned_data
