# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 商城首页内容URL配置模块 }
# @Date: 2021/05/22 21:51
from . import views
from django.conf.urls import url


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index')
]