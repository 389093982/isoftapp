# -*- coding: utf-8 -*-

from django.shortcuts import HttpResponseRedirect

try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x

class LoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 登录页面和 admin 页面无需拦截
        print(request.path)
        if request.path != '/account/login/' and '/admin/' not in request.path:
            if request.session.get('user', None):
                pass
            else:
                return HttpResponseRedirect('/account/login/')


