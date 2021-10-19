#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 订单序列化器模块 }
# @Date: 2021/10/19 20:47
from rest_framework import serializers
from goods.models import SKU
from orders.models import OrderInfo
from orders.models import OrderGoods


class OrderSimpleModelSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = OrderInfo
        fields = [
            'order_id',
            'create_time'
        ]


class SKUModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = [
            'name',
            'default_image',
        ]


class OrderGoodsModelSerializer(serializers.ModelSerializer):
    sku = SKUModelSerializer()

    class Meta:
        model = OrderGoods
        fields = [
            'count',
            'price',
            'sku',
        ]


class OrderInfoModelSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    skus = OrderGoodsModelSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = [
            'order_id',
            'user',
            'total_count',
            'total_amount',
            'freight',
            'pay_method',
            'status',
            'create_time',
            'skus',
        ]
