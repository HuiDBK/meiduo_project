# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 美多项目开发环境模块 }
# @Date: 2021/05/20 16:09
import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 追加子应用导包路径
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$a#@&!1cp3m%c)*zbzm*90y60%2ilgd^ra-49j48&+87#yz9@6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'meiduo_mall.apps.users'

    # 注册美多商城子应用
    'users',
    'contents',
    'verifications'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 指定项目异常中间件
    'meiduo_mall.utils.middlewares.ExceptionMiddleware'
]

ROOT_URLCONF = 'meiduo_mall.urls'

TEMPLATES = [

    # jinja2 模板引擎
    {
        # 'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'BACKEND': 'django.template.backends.jinja2.Jinja2',  # 换成jinja2模板引擎
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],

            # 补充Jinja2模板引擎环境
            'environment': 'meiduo_mall.utils.jinja2_env.jinja2_environment',
        },
    },

    # django 模板引擎
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    }
]

WSGI_APPLICATION = 'meiduo_mall.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }

    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # 'HOST': '192.168.246.133',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': '123456',
        'NAME': 'meiduo',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_USER_MODEL = 'users.User'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# 缓存别名
DEFAULT_CACHE_ALIAS = 'default'
SESSION_CACHE_ALIAS = "session"
VERIFY_CODE_CACHE_ALIAS = 'verify_code'

# 缓存
CACHES = {
    # 默认采用0号Redis库。
    DEFAULT_CACHE_ALIAS: {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.246.133:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },

    # session, 采用1号Redis库
    SESSION_CACHE_ALIAS: {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.246.133:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },

    # 校验码(图片、短信验证码), 采用2号Redis库
    VERIFY_CODE_CACHE_ALIAS: {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.246.133:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}

# celery 配置信息
CELERY_BROKER_URL = 'redis://192.168.246.133:6379/'

CELERY_RESULT_BACKEND = 'redis://192.168.246.133:6379/'

CELERY_RESULT_SERIALIZER = 'json'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

# 设置访问静态文件的url前缀
STATIC_URL = '/static/'

# 设置静态文件存放的目录
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# 日志器名称
LOGGER_NAME = 'django'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器

    # 日志信息显示的格式
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },

    # 对日志进行过滤
    'filters': {
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },

    # 日志处理方法
    'handlers': {

        # 向终端中输出日志
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },

        # 向文件中输出日志
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',

            # 日志文件的位置
            'filename': os.path.join(os.path.dirname(BASE_DIR), 'logs/meiduo.log'),
            'encoding': 'utf-8',
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },

    # 日志器
    'loggers': {
        LOGGER_NAME: {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    }
}
