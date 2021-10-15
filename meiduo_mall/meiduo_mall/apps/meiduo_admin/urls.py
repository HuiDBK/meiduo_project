#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 美多后台管理路由配置 }
# @Date: 2021/10/14 15:05
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter
from meiduo_admin.views import statistical
from meiduo_admin.views import users
from meiduo_admin.views import specs

urlpatterns = [

    # 登录
    url(r'^authorizations/$', obtain_jwt_token),

    # --------------  数据统计 -----------------
    # 用户总量
    url(r'^statistical/total_count/$', statistical.UserCountView.as_view()),
    # 日增用户
    url(r'^statistical/day_increment/$', statistical.UserDayCountView.as_view()),
    # 日活用户
    url(r'^statistical/day_active/$', statistical.UserDayActiveCountView.as_view()),
    # 下单用户
    url(r'^statistical/day_orders/$', statistical.UserDayOrdersCountView.as_view()),
    # 月增用户
    url(r'^statistical/month_increment/$', statistical.UserMonthCountView.as_view()),
    # 商品分类当日访问量
    url(r'^statistical/goods_day_views/$', statistical.UserGoodsCountView.as_view()),

    # ------------- 用户管理路由 --------------
    url(r'^users/$', users.UserView.as_view()),

    # ------------规格路由表-----------
    url(r'^goods/simple/$', specs.SpecsView.as_view({'get': 'simple'})),
]


# ----------规格表路由------
router = DefaultRouter()
router.register('goods/specs', specs.SpecsView, basename='specs')
urlpatterns += router.urls
