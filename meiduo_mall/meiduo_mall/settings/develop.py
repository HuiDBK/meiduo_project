# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 美多项目开发环境模块 }
# @Date: 2021/05/20 16:09
import os
import sys
import datetime

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

ALLOWED_HOSTS = [
    '127.0.0.1',
    'meiduo.site',
]

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
    'verifications',
    'oauth',
    'areas',
    'goods',
    'haystack',  # 全文检索
    'django_crontab',  # 定时任务
    'carts',
    'orders',
    'payment',
    'meiduo_admin',  # 美多后台管理模块
    'corsheaders',  # 跨域请求扩展
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
    'meiduo_mall.utils.middlewares.ExceptionMiddleware',

    # 跨域请求中间件
    'corsheaders.middleware.CorsMiddleware',
]

# 配置跨域请求白名单
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8080',
    'http://localhost:8080',
    'http://www.meiduo.site:8080',
    'http://api.meiduo.site:8000'
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

# jwt 认证有效期 1天
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'meiduo_admin.utils.jwt_response_payload_handler',
}

CORS_ALLOW_CREDENTIALS = True  # 允许携带cookie

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

        # 'OPTIONS': {
        #     'init_command': 'SET foreign_key_checks = 0;'
        # },
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

# 指定user认证模型类和认证后端
AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = ['users.utils.UsernameMobileAuthBackend']

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

# redis 缓存 ip/port 信息
REDIS_URI = f"redis://192.168.246.133:6379"

# 缓存别名
DEFAULT_CACHE_ALIAS = 'default'
SESSION_CACHE_ALIAS = "session"
VERIFY_CODE_CACHE_ALIAS = 'verify_code'
HISTORY_CACHE_ALIAS = 'history'
CARTS_CACHE_ALIAS = 'carts'

# 缓存
CACHES = {
    # 默认采用0号Redis库。
    DEFAULT_CACHE_ALIAS: {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"{REDIS_URI}/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },

    # session, 采用1号Redis库
    SESSION_CACHE_ALIAS: {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"{REDIS_URI}/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },

    # 校验码(图片、短信验证码), 采用2号Redis库
    VERIFY_CODE_CACHE_ALIAS: {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"{REDIS_URI}/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },

    # 用户浏览记录缓存, 采用3号Redis库
    HISTORY_CACHE_ALIAS: {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"{REDIS_URI}/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },

    # 购物车缓存, 采用4号Redis库
    CARTS_CACHE_ALIAS: {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"{REDIS_URI}/4",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}

# celery 配置信息
CELERY_BROKER_URL = f'{REDIS_URI}/'

CELERY_RESULT_BACKEND = f'{REDIS_URI}/'

CELERY_RESULT_SERIALIZER = 'json'

# 阿里支付宝沙箱应用ID
ALIPAY_APPID = '2021000116684030'

# 应用私钥文件路径
APP_PRIVATE_KEY_PATH = os.path.join(BASE_DIR, 'apps/payment/keys/app_private_key.pem')

# 阿里支付公钥路径
ALIPAY_PUBLIC_KEY_PATH = os.path.join(BASE_DIR, 'apps/payment/keys/alipay_public_key.pem')

# 设置阿里沙箱调试模式
ALIPAY_DEBUG = True

# 阿里支付页面地址
ALIPAY_URL = 'https://openapi.alipaydev.com/gateway.do'
ALIPAY_RETURN_URL = 'http://127.0.0.1:8000/payment/status/'

# 指定登录的url, 访问没权限的页面自动跳转到登录页面
LOGIN_URL = '/login'

# 获取Gitee登录页url
GITEE_CLIENT_ID = 'af47db9844c1be9689856551b3d224b10fce2c3d91cc3e5b1b9931537b360e9d'
GITEE_SECRET = '80198c78cc01398da70737ce724aabcaa58c010888b780a9f5c2d0a102039ad8'
GITEE_REDIRECT_URI = 'http://127.0.0.1:8000/gitee/oauth_back'
GITEE_LOGIN_URL = f'https://gitee.com/oauth/authorize?client_id={GITEE_CLIENT_ID}' \
                  f'&redirect_uri={GITEE_REDIRECT_URI}&response_type=code'

# 邮箱服务器的配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # 指定邮件后端
EMAIL_HOST = 'smtp.163.com'  # 发邮件主机
EMAIL_PORT = 25  # 发邮件端口
EMAIL_HOST_USER = 'huidbk@163.com'  # 授权的邮箱
EMAIL_HOST_PASSWORD = 'ZCSRRQDZCJEDWFCL'  # 邮箱授权时获得的密码，非注册登录密码
EMAIL_FROM = '美多商城<huidbk@163.com>'  # 发件人抬头

# 邮箱验证链接
EMAIL_VERIFY_URL = 'http://127.0.0.1:8000/emails/verification/'

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

# 指定自定义的Django文件存储类
DEFAULT_FILE_STORAGE = 'meiduo_mall.utils.fastdfs.fdfs_storage.FastDFSStorage'

# FastDFS相关参数
FDFS_BASE_URL = 'http://192.168.246.133:8888/'
# FDFS_BASE_URL = 'http://image.meiduo.site:8888/'

FASTDFS_PATH = os.path.join(BASE_DIR, 'utils/fastdfs/client.conf')

# Haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://192.168.246.133:9200/',  # Elasticsearch服务器ip地址，端口号固定为9200
        'INDEX_NAME': 'meiduo_mall',  # Elasticsearch建立的索引库的名称
    },
}

# 当添加、修改、删除数据时，自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# 全文检索每页数据个数
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 5

# 定时器配置
CRONJOBS = [
    # 每1分钟生成一次首页静态文件
    ('*/1 * * * *', 'contents.crons.generate_static_index_html',
     '>> ' + os.path.join(os.path.dirname(BASE_DIR), 'logs/crontab.log'))
]

# 指定中文编码格式
CRONTAB_COMMAND_PREFIX = 'LANG_ALL=zh_cn.UTF-8'

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
