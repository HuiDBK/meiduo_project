#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 购物车模块路由配置 }
# @Date: 2021/10/09 20:23
from django.conf.urls import url
from carts import views

urlpatterns = [
    url(r'^carts/$', views.CartsView.as_view(), name='info'),
    url(r'^carts/selection/$', views.CartsSelectAllView.as_view()),
    url(r'^carts/simple/$', views.CartsSimpleView.as_view()),
]

