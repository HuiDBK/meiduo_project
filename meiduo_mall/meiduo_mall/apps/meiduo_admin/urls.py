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
from meiduo_admin.views import images
from meiduo_admin.views import skus
from meiduo_admin.views import spus
from meiduo_admin.views import channels

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

    # ------------ 规格路由表 -----------
    url(r'^goods/simple/$', specs.SpecsView.as_view({'get': 'simple'})),

    # ------------ 图片路由 ------------
    url(r'^skus/simple/$', images.ImagesView.as_view({'get': 'simple'})),

    # ------------ sku路由 ------------
    url(r'^goods/(?P<pk>\d+)/specs/$', skus.SKUView.as_view({'get': 'specs'})),

    # ------------ spu路由 ------------
    url(r'^goods/brands/simple/$', spus.SPUView.as_view({'get': 'simple'})),
    url(r'^goods/channel/categories/$', spus.ChannelCategorysView.as_view()),
    url(r'^goods/channel/categories/(?P<id>\d+)/$', spus.ChannelCategorysView.as_view()),

    # ------------ 频道路由 ------------
    url(r'^goods/channels/$', channels.GoodsChannelsView.as_view(actions={
        'get': 'list',
        'post': 'create',
    })),

    url(r'^goods/channels/(?P<pk>\d+)/$', channels.GoodsChannelsView.as_view(actions={
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    })),

    url(r'^goods/categories/$', channels.CategoriesView.as_view()),

    url(r'^goods/channel_types/$', channels.GoodsChannelGroupView.as_view()),

    # 品牌路由
    url(r'^goods/brands/$', channels.BrandView.as_view(actions={
        'get': 'list',
        'post': 'create',
    })),

    url(r'^goods/brands/(?P<pk>\d+)/$', channels.BrandView.as_view(actions={
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),

]

# ---------- 规格表路由 -------
router = DefaultRouter()
router.register('goods/specs', specs.SpecsView, basename='specs')
urlpatterns += router.urls

# ------- 图片表路由 -------
router = DefaultRouter()
router.register('skus/images', images.ImagesView, basename='images')
urlpatterns += router.urls

# ------- SKU表路由 -------
router = DefaultRouter()
router.register('skus', skus.SKUView, basename='skus')
urlpatterns += router.urls

# ------- SPU表路由 -------
router = DefaultRouter()
router.register('goods', spus.SPUView, basename='goods')
urlpatterns += router.urls
