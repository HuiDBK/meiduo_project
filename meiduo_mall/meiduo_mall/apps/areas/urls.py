#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 省市区三级联动 url 配置模块 }
# @Date: 2021/10/05 15:36
from django.conf.urls import url
from . import views

urlpatterns = [
    url('^areas/$', views.AreasView.as_view())
]

