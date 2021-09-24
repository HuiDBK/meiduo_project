#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 验证码校验模块 url 配置 }
# @Date: 2021/09/24 19:53
from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'image_codes/(?P<uuid>[\w-]+)/', views.ImageCodeView.as_view()),
    url(r'sms_codes/(?P<mobile>1[3-9]\d{9})/', views.SMSCodeView.as_view())
]
