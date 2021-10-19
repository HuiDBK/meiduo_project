#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 后台订单管理视图 }
# @Date: 2021/10/19 20:45
from rest_framework.viewsets import ModelViewSet
from orders.models import OrderInfo
from meiduo_admin.utils import PageNum
from meiduo_admin.serializers.orders import OrderSimpleModelSerializer
from meiduo_admin.serializers.orders import OrderInfoModelSerializer


class OrderViewSet(ModelViewSet):
    queryset = OrderInfo.objects.all()
    serializer_class = OrderSimpleModelSerializer
    pagination_class = PageNum

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if keyword:
            return self.queryset.filter(order_id__contains=keyword)

        return self.queryset.all()

    def get_serializer_class(self):

        if self.action == 'list':
            return OrderSimpleModelSerializer
        elif self.action == 'retrieve':
            return OrderInfoModelSerializer
        elif self.action == 'partial_update':
            return OrderInfoModelSerializer
        else:
            return self.serializer_class
