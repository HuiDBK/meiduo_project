#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 模块描述 }
# @Date: 2021/10/19 17:13
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from goods.models import Brand
from meiduo_admin.utils import PageNum
from meiduo_admin.serializers.spus import BrandSerializer


class BrandView(ModelViewSet):
    """
    商品品牌视图
    """

    serializer_class = BrandSerializer
    queryset = Brand.objects.all()
    pagination_class = PageNum
    permission_classes = [IsAdminUser]
