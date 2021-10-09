import re

from django import http
from django.views import View
from django.conf import settings
from django.contrib.auth import login
from django_redis import get_redis_connection
from django.shortcuts import redirect, render

from users.models import User
from users.constants import USERNAME_COOKIE_EXPIRES
from oauth.models import OAuthGiteeUser
from oauth.utils import get_gitee_user_id
from oauth.utils import check_access_token
from oauth.utils import generate_access_token
from oauth.utils import get_gitee_access_token
from carts.utils import merge_cart_cookie_to_redis

from meiduo_mall.utils.constants import RedisKey
from meiduo_mall.utils.constants import CookieKey
from meiduo_mall.utils.enums import StatusCodeEnum
from meiduo_mall.utils.constants import HtmlTemplate
from meiduo_mall.utils.exceptions import BusinessException


# /gitee/oauth_back
class GiteeOAuthBackView(View):
    """
    Gitee 授权成功回调视图
    """

    def get(self, request):
        # 获取Gitee提供的授权码
        code = request.GET.get('code')
        if not code:
            return http.HttpResponseForbidden('缺少code')

        # 通过code换取access_token
        access_token = get_gitee_access_token(code)

        # 通过access_token获取 gitee用户信息
        gitee_uid = get_gitee_user_id(access_token)

        # 判断美多商城用户是否绑定gitee用户id
        try:
            gitee_user = OAuthGiteeUser.objects.get(gitee_uid=gitee_uid)
        except OAuthGiteeUser.DoesNotExist:
            # 未绑定, 跳转到美多商城用户信息绑定
            access_token_id = generate_access_token(gitee_uid)
            context = {'access_token_id': access_token_id}
            return render(request, HtmlTemplate.OAUTH_CALLBACK_HTML, context)
        else:
            # 已绑定用户状态保持
            user = gitee_user.user
            login(request, user)

            # 响应结果
            next = request.GET.get('state')  # 获取用户是从哪个页面跳转过来登录的
            response = redirect(next)

            # 登录时用户名写入到cookie，有效期15天
            response.set_cookie(CookieKey.USERNAME_KEY, user.username, max_age=USERNAME_COOKIE_EXPIRES)

            # 合并购物车
            response = merge_cart_cookie_to_redis(request=request, user=user, response=response)
            return response

    def post(self, request):
        """美多商城用户绑定到openid"""
        # 接收参数
        mobile = request.POST.get('mobile')
        pwd = request.POST.get('password')
        sms_code_client = request.POST.get('sms_code')
        access_token = request.POST.get('access_token_id')

        # 校验参数
        # 判断参数是否齐全
        if not all([mobile, pwd, sms_code_client]):
            raise BusinessException(StatusCodeEnum.NECESSARY_PARAM_ERR)

        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            raise BusinessException(StatusCodeEnum.MOBILE_ERR)

        # 判断密码是否合格
        if not re.match(r'^[0-9A-Za-z]{8,20}$', pwd):
            raise BusinessException(StatusCodeEnum.PWD_ERR)

        # 判断短信验证码是否一致
        redis_conn = get_redis_connection(settings.VERIFY_CODE_CACHE_ALIAS)
        sms_code_key = RedisKey.SMS_CODE_KEY.format(mobile=mobile)
        sms_code_server = redis_conn.get(sms_code_key)

        if sms_code_server is None:
            return render(request, HtmlTemplate.OAUTH_CALLBACK_HTML, {'sms_code_errmsg': '无效的短信验证码'})

        if sms_code_client != sms_code_server.decode():
            return render(request, HtmlTemplate.OAUTH_CALLBACK_HTML, {'sms_code_errmsg': '输入短信验证码有误'})

        # 判断openid是否有效：错误提示放在sms_code_errmsg位置
        gitee_uid = check_access_token(access_token)
        if not gitee_uid:
            return render(request, HtmlTemplate.OAUTH_CALLBACK_HTML, {'openid_errmsg': '无效的openid'})

        # 保存注册数据
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            # 用户不存在,新建用户
            user = User.objects.create_user(username=mobile, password=pwd, mobile=mobile)
        else:
            # 如果用户存在，检查用户密码
            if not user.check_password(pwd):
                return render(request, HtmlTemplate.OAUTH_CALLBACK_HTML, {'account_errmsg': '用户名或密码错误'})

        # 将用户绑定openid
        OAuthGiteeUser.objects.create(gitee_uid=gitee_uid, user=user)

        # 实现状态保持
        login(request, user)

        # 响应绑定结果
        next = request.GET.get('state')
        response = redirect(next)

        # 登录时用户名写入到cookie，有效期15天
        response.set_cookie(CookieKey.USERNAME_KEY, user.username, max_age=USERNAME_COOKIE_EXPIRES)

        # 合并购物车
        response = merge_cart_cookie_to_redis(request=request, user=user, response=response)

        return response


# /gitee/login
class GiteeAuthView(View):
    """
    Gitee 认证登录视图
    """

    def get(self, request):
        # next表示从哪个页面进入到的登录页面，将来登录成功后，就自动回到那个页面
        next = request.GET.get('next')

        # 获取Gitee登录页url
        login_url = settings.GITEE_LOGIN_URL + f'&state={next}'

        context = {
            'login_url': login_url
        }
        return http.JsonResponse(context)
