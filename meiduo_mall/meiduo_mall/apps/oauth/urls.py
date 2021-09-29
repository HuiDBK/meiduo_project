#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { oauth认证 url配置模块 }
# @Date: 2021/09/29 11:10
from oauth import views
from django.conf.urls import url

urlpatterns = [
    url(r'^gitee/login', view=views.GiteeAuthView.as_view(), name='gitee'),
    url(r'^gitee/oauth_back', view=views.GiteeOAuthBackView.as_view(), name='oauth_back')

]
