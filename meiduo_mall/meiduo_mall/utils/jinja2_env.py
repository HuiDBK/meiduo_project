# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { Jinja2模板引擎环境配置模块 }
# @Date: 2021/05/20 16:33

from jinja2 import Environment
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse


# 确保可以使用模板引擎中的{{ url('') }} {{ static('') }}这类语句
def jinja2_environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env
