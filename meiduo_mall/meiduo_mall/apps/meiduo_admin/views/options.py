#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 规格选项视图模块 }
# @Date: 2021/10/19 20:13
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from goods.models import SpecificationOption
from goods.models import SPUSpecification
from meiduo_admin.utils import PageNum
from meiduo_admin.serializers.options import OptModelSerializer
from meiduo_admin.serializers.options import SpecOptModelSerializer


class OptViewSet(ModelViewSet):
    queryset = SpecificationOption.objects.all()
    serializer_class = OptModelSerializer
    pagination_class = PageNum


class SpecSimpleListView(ListAPIView):
    queryset = SPUSpecification.objects.all()
    serializer_class = SpecOptModelSerializer
