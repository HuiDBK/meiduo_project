# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 用户模块URL配置 }
# @Date: 2021/05/22 13:38
from . import views
from django.conf.urls import url


urlpatterns = [
    url(r'^register$', views.RegisterView.as_view(), name='register'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^info/$', views.UserInfoView.as_view(), name='info'),
    url(r'^emails/$', views.EmailView.as_view(), name='emails'),
    url(r'^emails/verification/$', views.VerifyEmailView.as_view()),
    url(r'^addresses$', views.AddressView.as_view(), name='address'),
    url(r'^addresses/create/$', views.CreateAddressView.as_view()),
    url(r'^addresses/(?P<address_id>\d+)/$', views.UpdateDestroyAddressView.as_view()),
    url(r'^addresses/(?P<address_id>\d+)/default/$', views.DefaultAddressView.as_view()),
    url(r'^addresses/(?P<address_id>\d+)/title/$', views.UpdateTitleAddressView.as_view()),
    url(r'^password/$', views.ChangePasswordView.as_view(), name='password'),
    url(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', views.UsernameCountView.as_view()),
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
    url(r'^browse_histories/$', views.UserBrowseHistory.as_view()),
]

