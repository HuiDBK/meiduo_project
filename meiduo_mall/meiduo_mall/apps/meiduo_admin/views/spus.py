#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 后台SPU管理 }
# @Date: 2021/10/19 15:43
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from meiduo_admin.utils import PageNum
from meiduo_admin.serializers.spus import SPUSerializer
from meiduo_admin.serializers.spus import BrandSerializer
from meiduo_admin.serializers.spus import CateSimpleSerializer
from goods.models import SPU
from goods.models import Brand
from goods.models import GoodsCategory


class SPUView(ModelViewSet):
    serializer_class = SPUSerializer

    queryset = SPU.objects.all()

    pagination_class = PageNum

    permission_classes = [IsAdminUser]

    def simple(self, request):
        brands = Brand.objects.all()
        ser = BrandSerializer(brands, many=True)
        return Response(ser.data)


class ChannelCategorysView(ListAPIView):
    queryset = GoodsCategory.objects.all()
    serializer_class = CateSimpleSerializer

    def get_queryset(self):
        parent_id = self.kwargs.get('id')
        if parent_id:
            return self.queryset.filter(parent_id=parent_id)

        return self.queryset.filter(parent=None)
