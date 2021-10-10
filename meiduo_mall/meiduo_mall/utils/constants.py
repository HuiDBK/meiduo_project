#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 项目公共常量模块 }
# @Date: 2021/09/25 15:57

class HtmlTemplate(object):
    """
    项目 html网页模板路径汇总类
    """

    # 首页
    INDEX_HTML = 'index.html'

    """
    用户登录模块
    """
    # 用户登录
    LOGIN_HTML = 'users/login.html'

    # 用户注册
    REGISTER_HTML = 'users/register.html'

    # 用户中心个人信息
    USER_CENTER_INFO_HTML = 'users/user_center_info.html'

    # 用户中心收货地址
    USER_CENTER_ADDRESS_HTML = 'users/user_center_site.html'

    # 用户修全部订单

    # 用户中心修改密码
    USER_CENTER_PASS_HTML = 'users/user_center_pass.html'

    """
    OAuth 模块
    """
    # OAuth 第三方登录用户绑定
    OAUTH_CALLBACK_HTML = 'oauth/oauth_callback.html'

    """
    商品模块
    """
    # 商品列表
    GOODS_LIST_HTML = 'goods/list.html'

    # 商品详情
    GOODS_DETAIL_HTML = 'goods/detail.html'

    """
    全文检索模块
    """
    # 全文检索回调的 search.html
    SEARCH_HTML = 'search/search.html'

    """
    购物车模块
    """
    # 购物车列表
    CART_LIST_HTML = 'carts/cart.html'

    """
    订单模块
    """
    # 订单结算界面
    ORDER_PLACE_HTML = 'orders/place_order.html'

    """
    项目错误 html 模板
    """
    ERRORS_404_HTML = 'errors/404.html'


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
