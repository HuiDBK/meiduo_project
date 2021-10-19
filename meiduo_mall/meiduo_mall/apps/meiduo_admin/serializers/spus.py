#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { SPU序列化器模块 }
# @Date: 2021/10/19 15:47
from goods.models import SPU
from goods.models import Brand
from goods.models import GoodsCategory
from rest_framework import serializers


class BrandSerializer(serializers.ModelSerializer):
    """
    商品品牌 序列化器
    """

    class Meta:
        model = Brand
        fields = ['id', 'name']


class SPUSerializer(serializers.ModelSerializer):
    """
    SPU 序列化器
    """
    brand_id = serializers.IntegerField()
    brand = serializers.StringRelatedField(label='品牌')
    category1_id = serializers.IntegerField()
    category2_id = serializers.IntegerField()
    category3_id = serializers.IntegerField()

    class Meta:
        model = SPU
        fields = '__all__'


class CateSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = [
            'id',
            'name'
        ]
