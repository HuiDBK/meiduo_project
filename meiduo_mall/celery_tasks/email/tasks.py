#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 发送邮件异步任务模块 }
# @Date: 2021/10/01 22:00
import os
import logging
from django.conf import settings
from django.core.mail import send_mail
from celery_tasks.main import celery_app

logger = logging.getLogger(settings.LOGGER_NAME)


@celery_app.task(bind=True, name='celery_send_verify_email', retry_backoff=3)
def celery_send_verify_email(self, to_email, verify_url):
    """
    发送验证邮箱邮件
    :param self: 发送邮箱任务自身实例
    :param to_email: 收件人邮箱
    :param verify_url: 验证链接
    :return: None
    """
    subject = "美多商城邮箱验证"
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用美多商城。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (to_email, verify_url, verify_url)
    try:
        send_mail(
            subject=subject,
            message="",
            from_email=settings.EMAIL_FROM,
            recipient_list=[to_email],
            html_message=html_message
        )
    except Exception as e:
        logger.error(e)
        # 有异常自动重试三次
        raise self.retry(exc=e, max_retries=3)
