#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 视图工具类模块 }
# @Date: 2021/09/29 10:05
from functools import wraps
from django.contrib.auth.decorators import login_required
from meiduo_mall.utils.enums import StatusCodeEnum
from meiduo_mall.utils.exceptions import BusinessException


class LoginRequiredMixin(object):
    """验证用户是否登录扩展类"""

    @classmethod
    def as_view(cls, **initkwargs):
        # 自定义的as_view()方法中，调用父类的as_view()方法
        view = super().as_view()
        return login_required(view)


def login_required_json(view_func):
    """
    判断用户是否登录的装饰器，并返回json
    :param view_func: 被装饰的视图函数
    :return: json、view_func
    """

    # 恢复view_func的名字和文档
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        # 如果用户未登录，返回json数据
        if not request.user.is_authenticated:
            raise BusinessException(StatusCodeEnum.USER_ERR)
        else:
            # 如果用户登录，进入到view_func中
            return view_func(request, *args, **kwargs)

    return wrapper


class LoginRequiredJSONMixin(object):
    """验证用户是否登陆并返回json的扩展类"""

    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        return login_required_json(view)
