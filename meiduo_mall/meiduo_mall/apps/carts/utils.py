#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 购物车工具模块 }
# @Date: 2021/10/09 23:06
import pickle
import base64

from django.conf import settings
from django_redis import get_redis_connection

from meiduo_mall.utils.constants import CookieKey
from meiduo_mall.utils.constants import RedisKey


def merge_cart_cookie_to_redis(request, user, response):
    """
    登录后合并cookie购物车数据到Redis
    :param request: 本次请求对象，获取cookie中的数据
    :param response: 本次响应对象，清除cookie中的数据
    :param user: 登录用户信息，获取user_id
    :return: response
    """
    # 获取cookie中的购物车数据
    cookie_cart_str = request.COOKIES.get(CookieKey.CARTS_KEY)

    # cookie中没有数据就响应结果
    if not cookie_cart_str:
        return response
    cookie_cart_dict = pickle.loads(base64.b64decode(cookie_cart_str.encode()))

    new_cart_dict = {}
    new_cart_selected_add = []
    new_cart_selected_remove = []

    # 同步cookie中购物车数据
    for sku_id, cookie_dict in cookie_cart_dict.items():
        new_cart_dict[sku_id] = cookie_dict['count']

        if cookie_dict['selected']:
            new_cart_selected_add.append(sku_id)
        else:
            new_cart_selected_remove.append(sku_id)

    # 将new_cart_dict写入到Redis数据库
    redis_conn = get_redis_connection(settings.CARTS_CACHE_ALIAS)
    pl = redis_conn.pipeline()

    user_carts_key = RedisKey.USER_CARTS_KEY.format(user_id=user.id)
    pl.hmset(user_carts_key, new_cart_dict)

    # 将勾选状态同步到Redis数据库
    carts_selected_key = RedisKey.CARTS_SELECTED_KEY.format(user_id=user.id)
    if new_cart_selected_add:
        pl.sadd(carts_selected_key, *new_cart_selected_add)
    if new_cart_selected_remove:
        pl.srem(carts_selected_key, *new_cart_selected_remove)
    pl.execute()

    # 清除cookie
    response.delete_cookie(CookieKey.CARTS_KEY)

    return response
