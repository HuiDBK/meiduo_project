# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 用户模块URL配置 }
# @Date: 2021/05/22 13:38
from . import views
from django.conf.urls import url


urlpatterns = [
    url(r'^register$', views.RegisterView.as_view(), name='register'),
]

