#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 订单模块路由配置 }
# @Date: 2021/10/10 12:53
from django.conf.urls import url
from orders import views

urlpatterns = [
    url(r'^orders/settlement/$', views.OrderSettlementView.as_view(), name='settlement'),
]
