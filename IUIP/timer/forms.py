# -*- coding: utf-8 -*-

# 集成配置环境表单
from django import forms

from index.models import Environment
from resources.models import Client
from timer.models import IntgList


class IntgConfigForm(forms.Form):
    def __init__(self,*args,**kwargs):
        super(IntgConfigForm,self).__init__(*args,**kwargs)
        self.fields['initial_deploy_env'].choices=((x.env_name,x.env_name) for x in Environment.objects.all())
        self.fields['source_client_name'].choices=((x.client_short_name,x.client_short_name) for x in Client.objects.all())
        self.fields['target_client_name'].choices=((x.client_short_name,x.client_short_name) for x in Client.objects.all())

    initial_deploy_env = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'style':'width:65%;'}),
                                           label='初次部署环境')
    source_client_name = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'style':'width:65%;'}),
                                           label='源系统名称')
    target_client_name = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'style':'width:65%;'}),
                                           label='宿系统名称')
    target_table_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style':'width:65%;'}),
                                        label='下游接口表名')
    business_meaning = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style':'width:65%;'}),
                                        label='集成业务含义')
    description = forms.CharField(widget=forms.Textarea(attrs={'style':'width:84%;height: 100px;'}),
                                 label='备注')
    def clean(self):
        cleaned_data = super(IntgConfigForm,self).clean()
        source_client_name_data = cleaned_data.get('source_client_name')
        target_client_name_data = cleaned_data.get('target_client_name')
        target_table_name_data = cleaned_data.get('target_table_name')
        business_meaning_data = cleaned_data.get('business_meaning')

        integration_point_name = ''.join(
            [source_client_name_data, '2', target_client_name_data, '(', target_table_name_data, ')_', business_meaning_data, '_Timer'])
        if source_client_name_data == target_client_name_data:
            msg = u'源宿系统不能相同!'
            self._errors['description'] = self.error_class([msg])
            del cleaned_data['description']
        elif IntgList.objects.filter(integration_point_name=integration_point_name).count() is not 0:
            msg = u'集成点已存在!'
            self._errors['description'] = self.error_class([msg])
            del cleaned_data['description']
        return cleaned_data



