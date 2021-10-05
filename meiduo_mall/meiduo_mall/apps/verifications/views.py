# 内置库
import logging

# 第三方库
from django import http
from django.views import View
from django_redis import get_redis_connection
from celery_tasks.sms.tasks import celery_send_sms_code

# 自建库
from meiduo_mall import settings
from meiduo_mall.utils import sms
from meiduo_mall.utils.result import R
from meiduo_mall.utils.constants import RedisKey
from meiduo_mall.utils.enums import StatusCodeEnum
from verifications import constants
from verifications.libs.captcha import captcha

logger = logging.getLogger(name=settings.LOGGER_NAME)


# image_codes/(?P<uuid>[\w-]+)/
class ImageCodeView(View):
    """图形验证码视图"""

    def get(self, request, uuid):
        """
        :param request: 请求对象
        :param uuid: 图片验证码唯一标识
        :return: image/jpg
        """

        # 生成图片验证码
        text, image = captcha.generate_captcha()
        logger.info(text)

        # 保存到redis中 meiduo:img:code:uuid -> text
        redis_cli = get_redis_connection(alias=settings.VERIFY_CODE_CACHE_ALIAS)
        img_code_key = RedisKey.IMG_CODE_KEY.format(uuid=uuid)
        redis_cli.setex(img_code_key, constants.IMAGE_CODE_REDIS_EXPIRES, text)

        # 响应图形验证码
        return http.HttpResponse(image, content_type='image/jpg')


# sms_codes/(?P<mobile>1[3-9]\d{9})/
class SMSCodeView(View):
    """
    短信验证码类视图
    """

    def get(self, request, mobile):
        """
        :param request: 请求对象
        :param mobile: 手机号
        :return: json
        """

        # 接受参数
        image_code_client = request.GET.get('image_code')
        uuid = request.GET.get('uuid')

        # 校验参数
        if not all([image_code_client, uuid]):
            context = R.set_result(StatusCodeEnum.NECESSARY_PARAM_ERR).data()
            return http.JsonResponse(context)

        # 创建连接到redis的对象
        redis_conn = get_redis_connection(settings.VERIFY_CODE_CACHE_ALIAS)

        # 判断用户是否频繁发送短信验证码 meiduo:sms:send:flag:{mobile}
        sms_send_flag_key = RedisKey.SMS_SEND_FLAG_KEY.format(mobile=mobile)  # 发送短信验证码的标记
        send_flag = redis_conn.get(sms_send_flag_key)
        if send_flag:
            context = R.set_result(StatusCodeEnum.THROTTLING_ERR).data()
            return http.JsonResponse(context)

        # 提取图形验证码 meiduo:img:code:{uuid}
        img_code_key = RedisKey.IMG_CODE_KEY.format(uuid=uuid)
        image_code_server = redis_conn.get(img_code_key)
        if image_code_server is None:
            # 图形验证码过期或者不存在
            context = R.set_result(StatusCodeEnum.IMAGE_CODE_ERR).data()
            return http.JsonResponse(context)

        # 删除图形验证码，避免恶意测试图形验证码
        redis_conn.delete(img_code_key)

        # 对比图形验证码
        image_code_server = image_code_server.decode()  # bytes转字符串
        if image_code_client.lower() != image_code_server.lower():  # 转小写后比较
            context = R.set_result(StatusCodeEnum.IMAGE_CODE_ERR).data()
            return http.JsonResponse(context)

        # 生成短信验证码
        sms_code = sms.generate_sms_code()
        logger.info(f'sms_code:{sms_code}')

        # 创建redis管道
        pl = redis_conn.pipeline()
        sms_code_key = RedisKey.SMS_CODE_KEY.format(mobile=mobile)

        # 保存短信验证码 meiduo:sms:code:{mobile}
        pl.setex(sms_code_key, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # 保存发送短信验证码的标记
        pl.setex(sms_send_flag_key, constants.SEND_SMS_CODE_INTERVAL, 1)
        pl.execute()

        # 发送短信验证码
        # sms.send_message(mobile, sms_code)
        celery_send_sms_code.delay(mobile, sms_code)    # 使用 celery 异步发送短信

        context = R.ok().data()
        return http.JsonResponse(context)
