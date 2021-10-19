#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 规格选项序列化器模块 }
# @Date: 2021/10/19 20:16
from rest_framework import serializers
from goods.models import SPUSpecification
from goods.models import SpecificationOption


class OptModelSerializer(serializers.ModelSerializer):
    spec = serializers.StringRelatedField()
    spec_id = serializers.IntegerField()

    class Meta:
        model = SpecificationOption
        fields = [
            'id',
            'spec',
            'value',
            'spec_id'
        ]


class SpecOptModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPUSpecification
        fields = [
            'id',
            'name',
        ]
