#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 频道模块序列化器 }
# @Date: 2021/10/19 19:20
from rest_framework import serializers
from goods.models import Brand
from goods.models import GoodsChannel
from goods.models import GoodsCategory
from goods.models import GoodsChannelGroup


class GoodsChannelModelSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    category_id = serializers.IntegerField()
    group = serializers.StringRelatedField()
    group_id = serializers.IntegerField()

    class Meta:
        model = GoodsChannel

        fields = [
            'id',
            'category',
            'category_id',
            'group',
            'group_id',
            'url',
            'sequence',
        ]


class GoodsCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsChannelGroupModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsChannelGroup
        fields = '__all__'


class BrandModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
