#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 项目公共常量模块 }
# @Date: 2021/09/25 15:57


class RedisKey(object):
    """
    redis key 常量设计类
    """
    # 图形验证码 key
    IMG_CODE_KEY = 'meiduo:img:code:{uuid}'

    # 短信验证码 key
    SMS_CODE_KEY = 'meiduo:sms:code:{mobile}'

    # 短信发送标记
    SMS_SEND_FLAG_KEY = 'meiduo:sms:send:flag:{mobile}'

    # 省份数据 key
    PROVINCES_KEY = 'meiduo:area:provinces'

    # 市区数据 key
    SUB_AREA_KEY = 'meiduo:sub_area:{area_id}'

    # 用户商品浏览记录
    HISTORY_BROWSE_KEY = 'meiduo:history:{user_id}'
