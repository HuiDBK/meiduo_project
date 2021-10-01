#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { Celery入口模块 }
# @Date: 2021/09/26 12:39
import os
from celery import Celery

# 为celery使用django配置文件进行设置
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ["DJANGO_SETTINGS_MODULE"] = "meiduo_mall.settings.develop"

# 创建Celery实例
celery_app = Celery('meiduo_celery')

# 加载celery配置文件 设置 broker 消息队列
celery_app.config_from_object('celery_tasks.config')

# 配置 celery 异步任务包，进行自动注册 celery 异步任务
task_packages = [
    'celery_tasks.sms',
    'celery_tasks.email'
]
celery_app.autodiscover_tasks(packages=task_packages)
