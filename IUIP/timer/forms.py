# -*- coding: utf-8 -*-

from django import forms

from index.models import Environment
from resources.models import Client
from timer.models import IntgList


# 集成配置环境表单
class IntgConfigForm(forms.Form):

    def __init__(self,*args,**kwargs):
        super(IntgConfigForm,self).__init__(*args,**kwargs)
        self.fields['initial_deploy_env'].choices= ((x.env_name,x.env_name) for x in Environment.objects.all())
        self.fields['source_client_name'].choices= ((x.client_short_name,x.client_short_name) for x in Client.objects.all())
        self.fields['target_client_name'].choices= ((x.client_short_name,x.client_short_name) for x in Client.objects.all())

    initial_deploy_env = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), label='初次部署环境')
    source_client_name = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), label='源系统名称')
    target_client_name = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), label='宿系统名称')
    target_table_name = forms.CharField(label='下游接口表名', error_messages={'required':u'参数不能为空'})
    business_meaning = forms.CharField(label='集成业务含义', error_messages={'required':u'参数不能为空'})
    descript = forms.CharField(label='备注', error_messages={'required':u'参数不能为空'})

    def clean(self):
        cleaned_data = super(IntgConfigForm,self).clean()
        source_client_name_data = cleaned_data.get('source_client_name', '')
        target_client_name_data = cleaned_data.get('target_client_name', '')
        initial_deploy_env_data = cleaned_data.get('initial_deploy_env', '')
        target_table_name_data = cleaned_data.get('target_table_name', '')
        business_meaning_data = cleaned_data.get('business_meaning', '')
        descript = cleaned_data.get('descript', '')

        if len(target_table_name_data.strip()) == 0:
            msg = u'下游接口表名不能相同!'
            self._errors['target_table_name'] = self.error_class([msg])
            if 'target_table_name' in cleaned_data:
                del cleaned_data['target_table_name']

        if len(business_meaning_data.strip()) == 0:
            msg = u'集成业务含义不能相同!'
            self._errors['business_meaning'] = self.error_class([msg])
            if 'business_meaning' in cleaned_data:
                del cleaned_data['business_meaning']

        if len(descript.strip()) == 0:
            msg = u'描述不能相同!'
            self._errors['descript'] = self.error_class([msg])
            if 'descript' in cleaned_data:
                del cleaned_data['descript']

        integration_point_name = ''.join(
            [source_client_name_data, '2', target_client_name_data, '(', target_table_name_data, ')_', business_meaning_data, '_Timer'])

        if source_client_name_data == target_client_name_data:
            msg = u'源宿系统不能相同!'
            self._errors['descript'] = self.error_class([msg])
            if 'descript' in cleaned_data:
                del cleaned_data['descript']
        elif IntgList.objects.filter(integration_point_name=integration_point_name).count() is not 0:
            msg = u'集成点已存在!'
            self._errors['descript'] = self.error_class([msg])
            if 'descript' in cleaned_data:
                del cleaned_data['descript']
        return cleaned_data



