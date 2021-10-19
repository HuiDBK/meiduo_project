#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 频道视图模块 }
# @Date: 2021/10/19 19:19
from rest_framework.viewsets import ModelViewSet
from goods.models import Brand
from goods.models import GoodsCategory
from meiduo_admin.serializers.channels import GoodsChannel
from meiduo_admin.serializers.channels import GoodsChannelGroup
from meiduo_admin.serializers.channels import GoodsCategoryModelSerializer
from meiduo_admin.serializers.channels import GoodsChannelModelSerializer
from meiduo_admin.serializers.channels import GoodsChannelGroupModelSerializer
from meiduo_admin.serializers.channels import BrandModelSerializer
from meiduo_admin.utils import PageNum
from rest_framework.generics import ListAPIView


class GoodsChannelsView(ModelViewSet):
    queryset = GoodsChannel.objects.all()
    serializer_class = GoodsChannelModelSerializer
    pagination_class = PageNum


class CategoriesView(ListAPIView):
    queryset = GoodsCategory.objects.filter(parent=None)
    serializer_class = GoodsCategoryModelSerializer


class GoodsChannelGroupView(ListAPIView):
    queryset = GoodsChannelGroup.objects.all()
    serializer_class = GoodsChannelGroupModelSerializer


class BrandView(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandModelSerializer
    pagination_class = PageNum
