#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 项目中间件模块 }
# @Date: 2021/09/24 8:18
import logging
from django.db import DatabaseError
from meiduo_mall.utils.result import R
from django.http.response import JsonResponse
from django.http import HttpResponseServerError
from meiduo_mall.utils.enums import StatusCodeEnum
from django.middleware.common import MiddlewareMixin
from meiduo_mall.utils.exceptions import BusinessException

logger = logging.getLogger('django')


class ExceptionMiddleware(MiddlewareMixin):
    """异常中间件"""

    def process_exception(self, request, exception):
        """
        统一异常处理
        :param request: 请求
        :param exception: 异常
        :return:
        """
        if isinstance(exception, BusinessException):
            # 业务异常处理
            data = R.set_result(exception.enum_cls).data()
            return JsonResponse(data)

        elif isinstance(exception, DatabaseError):
            # 数据库异常
            r = R.set_result(StatusCodeEnum.DB_ERR)
            logger.error(r.data(), exc_info=True)
            return HttpResponseServerError(StatusCodeEnum.SERVER_ERR.errmsg)

        elif isinstance(exception, Exception):
            # 服务器异常处理
            r = R.server_error()
            logger.error(r.data(), exc_info=True)
            return HttpResponseServerError(r.errmsg)
