#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 阿里支付模块路由配置 }
# @Date: 2021/10/11 22:30
from django.conf.urls import url
from payment import views

urlpatterns = [
    url(r'payment/(?P<order_id>\d+)/', views.PaymentView.as_view()),
    url(r'payment/status/', views.PaymentStatusView.as_view())
]
