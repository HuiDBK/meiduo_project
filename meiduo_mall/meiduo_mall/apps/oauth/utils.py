#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { oauth 认证工具模块 }
# @Date: 2021/09/29 13:01
import logging
import requests
from oauth import constants
from itsdangerous import BadData
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

logger = logging.getLogger(settings.LOGGER_NAME)


def check_access_token(access_token_openid):
    """
    反解、反序列化access_token_openid
    :param access_token_openid: openid密文
    :return: openid明文
    """
    # 创建序列化器对象：序列化和反序列化的对象的参数必须是一模一样的
    s = Serializer(settings.SECRET_KEY, constants.ACCESS_TOKEN_EXPIRES)

    # 反序列化openid密文
    try:
        data = s.loads(access_token_openid)
    except BadData:  # openid密文过期
        return None
    else:
        # 返回openid明文
        return data.get('gitee_uid')


def get_gitee_access_token(code):
    """
    通过 gitee授权码获取 access_token
    :param code:
    :return: access_token
    """
    url = 'https://gitee.com/oauth/token'
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': settings.GITEE_CLIENT_ID,
        'client_secret': settings.GITEE_SECRET,
        'redirect_uri': settings.GITEE_REDIRECT_URI
    }
    """
        {
        "access_token": "021077bd5a0942eba0e421efc16da68f",
        "token_type": "bearer",
        "expires_in": 86400,
        "refresh_token": "44e88569821a529c7a02be18e750b2916b65980d3b71012e3cef789b4efcec46",
        "scope": "user_info",
        "created_at": 1632892032
        }
    """
    response = requests.post(url, data=data)

    ret_dict = response.json()
    access_token = ret_dict.get('access_token')
    return access_token


def get_gitee_user_id(access_token):
    """
    获取 gitee 的用户信息
    :param access_token: gitee 授权令牌
    :return:
    """
    url = 'https://gitee.com/api/v5/user'
    params = {
        'access_token': access_token
    }
    response = requests.get(url=url, params=params)
    ret_dict = response.json()
    gitee_user_id = ret_dict.get('id')
    gitee_user_name = ret_dict.get('name')

    logger.info(f'gitee_user_id: {gitee_user_id}')
    logger.info(f'gitee_user_name: {gitee_user_name}')
    return gitee_user_id


def generate_access_token(gitee_uid):
    """
    签名、序列化 gitee_uid
    :param gitee_uid: 用户的 gitee_uid
    :return: access_token
    """
    serializer = Serializer(settings.SECRET_KEY, expires_in=constants.ACCESS_TOKEN_EXPIRES)
    data = {'gitee_uid': gitee_uid}
    token = serializer.dumps(data)
    return token.decode()
