#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 项目枚举类模块 }
# @Date: 2021/09/23 23:37

from enum import Enum


class StatusCodeEnum(Enum):
    """状态码枚举类"""

    OK = (0, '成功')
    ERROR = (-1, '服务器异常')

    IMAGECODEERR = (4001, '图形验证码错误')
    THROTTLINGERR = (4002, '访问过于频繁')
    NECESSARYPARAMERR = (4003, '缺少必传参数')
    USERERR = (4004, '用户名错误')
    PWDERR = (4005, '密码错误')
    CPWDERR = (4006, '密码不一致')
    MOBILEERR = (4007, '手机号错误')
    SMSCODERR = (4008, '短信验证码有误')
    ALLOWERR = (4009, '未勾选协议')
    SESSIONERR = (4010, '用户未登录')

    DBERR = (5000, '数据错误')
    EMAILERR = (5001, '邮箱错误')
    TELERR = (5002, '固定电话错误')
    NODATAERR = (5003, '无数据')
    NEWPWDERR = (5004, '新密码数据')
    OPENIDERR = (5005, '无效的openid')
    PARAMERR = (5006, '参数错误')
    STOCKERR = (5007, '库存不足')

    @property
    def code(self):
        """获取状态码"""
        return self.value[0]

    @property
    def errmsg(self):
        """获取状态码信息"""
        return self.value[1]
