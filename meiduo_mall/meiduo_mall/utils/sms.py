#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 发送短信验证码模块 }
# @Date: 2021/09/24 21:49
import json
import random
import logging
from ronglian_sms_sdk import SmsSDK

logger = logging.getLogger('django')

accId = '8a216da87ba59937017c1804686a1bf4'
accToken = '311e282f76914d1ab9f66dd314659efc'
appId = '8a216da87ba59937017c1804694f1bfa'
test_mobile = '13033221752'
tid = '1'
sms_code_ttl = 5  # 短信验证码有效时间 单位/分钟

sdk = SmsSDK(accId, accToken, appId)


def generate_sms_code():
    """
    随机生成6位短信验证码
    :return: sms_code
    """
    # 随机6位短信验证码
    sms_code = random.randint(100000, 999999)
    sms_code = list(str(sms_code))
    random.shuffle(sms_code)
    sms_code = ''.join(sms_code)
    return sms_code


def send_message(mobile, sms_code):
    """
    发送短信验证码
    :param mobile: 手机号
    :param sms_code: 要发送的短信验证码
    :return: True/False
    """
    logger.info(mobile)
    # 发送并获取响应信息
    datas = (sms_code, sms_code_ttl)
    mobile = test_mobile
    # 将短信验证码存入Redis，设置过期时间为sms_code_ttl
    # key   meiduo:sms:code:{13033221725}  123456 ttl
    resp_str = sdk.sendMessage(tid, mobile, datas)
    resp_dict = json.loads(resp_str)
    if resp_dict.get('statusCode', None) == '000000':
        # 发送成功
        return True
    else:
        return False


def main():
    send_message(test_mobile, generate_sms_code())


if __name__ == '__main__':
    main()
