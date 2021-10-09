#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 项目公共常量模块 }
# @Date: 2021/09/25 15:57

class CookieKey(object):
    """
    Cookie key 常量设计类
    """

    # 登录用户名 cookie key
    USERNAME_KEY = 'username'

    # 购物车信息 cookie key
    CARTS_KEY = 'carts'


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

    # 用户购物车数据 key
    USER_CARTS_KEY = 'meiduo:carts:{user_id}'

    # 购物车商品是否勾选 key
    CARTS_SELECTED_KEY = 'meiduo:cart:selected:{user_id}'
