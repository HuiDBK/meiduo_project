#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 美多后台管理路由配置 }
# @Date: 2021/10/14 15:05
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [

    url(r'^authorizations/$', obtain_jwt_token),
]
