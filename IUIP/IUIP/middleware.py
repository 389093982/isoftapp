# -*- coding: utf-8 -*-
from django.utils.deprecation import MiddlewareMixin


class UserMenuMiddlewareMixin(MiddlewareMixin):
    def process_request(self, request):
        if request.method == 'GET':
            menu_type = request.GET.get('menu_type', 'appid')
            request.session['menu_type'] = menu_type