#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 短信异步任务模块 }
# @Date: 2021/09/26 12:47
from .ronglian import send_sms_code
from celery_tasks.main import celery_app


# @celery_app.task 装饰器用于标识函数是celery异步任务好让 celery 自动搜寻异步任务
# bind：保证task对象会作为第一个参数自动传入
# name：异步任务别名
# retry_backoff：异常自动重试的时间间隔 第n次(retry_backoff×2^(n-1))s
# max_retries：异常自动重试次数的上限

@celery_app.task(bind=True, name='celery_send_sms_code', retry_backoff=3)
def celery_send_sms_code(self, mobile, sms_code):
    """
    celery 异步发送短信验证码
    :param self: 自身任务实例
    :param mobile: 手机号
    :param sms_code: 短信验证码内容
    :return: True 成功  False 失败
    """
    try:
        send_ret = send_sms_code(mobile, sms_code)
    except Exception as e:
        raise self.retry(exc=e, max_retries=3)

    if not send_ret:
        raise self.retry(exc=Exception('发送短信失败'), max_retries=3)
    return send_ret
