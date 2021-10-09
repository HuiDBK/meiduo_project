import re
import json
import logging

from django import http
from django.views import View
from django.conf import settings
from django.db import DatabaseError
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django_redis import get_redis_connection
from django.shortcuts import render, reverse, redirect

from users import constants
from users.models import User
from users.models import Address
from goods.models import SKU
from users.utils import generate_verify_email_url
from users.utils import check_verify_email_token
from meiduo_mall.utils.result import R
from meiduo_mall.utils.constants import RedisKey
from meiduo_mall.utils.enums import StatusCodeEnum
from meiduo_mall.utils.constants import HtmlTemplate
from meiduo_mall.utils.views import LoginRequiredMixin
from meiduo_mall.utils.views import LoginRequiredJSONMixin
from meiduo_mall.utils.exceptions import BusinessException
from celery_tasks.email.tasks import celery_send_verify_email

logger = logging.getLogger(settings.LOGGER_NAME)


# /register
class RegisterView(View):
    """用户注册类视图"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username = None
        self.password = None
        self.confirm_pwd = None
        self.mobile = None
        self.sms_code_client = None
        self.allow = None

    def get(self, request):
        """提供注册页面"""
        return render(request, HtmlTemplate.REGISTER_HTML)

    def verify_params(self, request):
        """
        校验注册信息
        :param request: 注册请求对象
        :return: response_ret
        """
        # 接受参数
        self.username = request.POST.get('username')
        self.password = request.POST.get('password')
        self.confirm_pwd = request.POST.get('confirm_pwd')
        self.mobile = request.POST.get('mobile')
        self.sms_code_client = request.POST.get('sms_code')
        self.allow = request.POST.get('allow')

        # 校验参数
        all_args = [
            self.username, self.password, self.confirm_pwd,
            self.mobile, self.sms_code_client, self.allow
        ]
        if not all(all_args):
            raise BusinessException(StatusCodeEnum.PARAM_ERR)

        # 用户名 5-20个字符
        if not re.match(r'^[a-zA-Z0-9_]{5,20}', self.username):
            raise BusinessException(StatusCodeEnum.USER_ERR)

        # 密码 8-20个字符
        if not re.match(r'^[a-zA-Z0-9]{8,20}', self.password):
            raise BusinessException(StatusCodeEnum.PWD_ERR)

        # 两次密码一致性
        if self.password != self.confirm_pwd:
            raise BusinessException(StatusCodeEnum.CPWD_ERR)

        # 手机号合法性
        if not re.match(r'^1[3-9]\d{9}$', self.mobile):
            raise BusinessException(StatusCodeEnum.MOBILE_ERR)

        # 是否勾选用户协议
        if self.allow != 'on':
            raise BusinessException(StatusCodeEnum.ALLOW_ERR)

    def post(self, request):
        """实现用户注册"""
        self.verify_params(request)

        # 短验证码是否一致
        redis_conn = get_redis_connection(alias=settings.VERIFY_CODE_CACHE_ALIAS)
        sms_code_key = RedisKey.SMS_CODE_KEY.format(mobile=self.mobile)
        sms_code_server = redis_conn.get(sms_code_key)

        if not sms_code_server:
            # 短信验证码失效
            # raise BusinessException(StatusCodeEnum.SMS_CODE_ERR)
            return render(request, 'users/register.html', {'sms_code_errmsg': '无效的短信验证码'})

        if sms_code_server.decode() != self.sms_code_client:
            # 短信验证码不一致
            # raise BusinessException(StatusCodeEnum.SMS_CODE_ERR)
            return render(request, 'users/register.html', {'sms_code_errmsg': '输入短信验证码有误'})

        # 保存注册数据
        try:
            user = User.objects.create_user(
                username=self.username,
                password=self.password,
                mobile=self.mobile,
            )
        except DatabaseError as e:
            logger.error(e)
            context = R.set_result(StatusCodeEnum.REGISTER_FAILED_ERR).data()
            return render(request, 'users/register.html', context)

        # 注册成功即保存用户状态
        login(request, user)

        # 响应结果
        return redirect(reverse('contents:index'))


# /login/
class LoginView(View):
    """用户名登录"""

    def get(self, request):
        """
        提供登录界面
        :param request: 请求对象
        :return: 登录界面
        """
        return render(request, HtmlTemplate.LOGIN_HTML)

    def post(self, request):
        """
        实现登录逻辑
        :param request: 请求对象
        :return: 登录结果
        """
        # 接受参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        remembered = request.POST.get('remembered')

        # 校验参数
        # 判断参数是否齐全
        if not all([username, password]):
            raise BusinessException(StatusCodeEnum.NECESSARY_PARAM_ERR)

        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            raise BusinessException(StatusCodeEnum.USER_ERR)

        # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            raise BusinessException(StatusCodeEnum.PWD_ERR)

        # 认证登录用户
        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, 'users/login.html', {'account_errmsg': '用户名或密码错误'})

        # 实现状态保持
        login(request, user)

        # 设置状态保持的周期
        if remembered != 'on':
            # 没有记住用户：浏览器会话结束就过期
            request.session.set_expiry(0)
        else:
            # 记住用户：None表示两周后过期
            request.session.set_expiry(None)

        # 响应登录结果
        redirect_url = request.GET.get('next')
        if redirect_url:
            response = redirect(redirect_url)
        else:
            response = redirect(reverse('contents:index'))

        # 登录时用户名写入到cookie，有效期15天
        # 为了实现在首页的右上角展示用户名信息，我们需要将用户名缓存到cookie中
        # response.set_cookie('key', 'val', 'expiry')
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)

        return response


# /logout
class LogoutView(View):
    """退出登录"""

    def get(self, request):
        """实现退出登录逻辑"""
        # 清理session
        logout(request)
        # 退出登录，重定向到登录页
        response = redirect(reverse('contents:index'))
        # 退出登录时清除cookie中的username
        response.delete_cookie('username')

        return response


# /usernames/(?P<username>)/count/
class UsernameCountView(View):
    """判断用户名是否重复注册"""

    def get(self, request, username):
        """
        :param request: 请求对象
        :param username: 用户名
        :return: json
        """

        count = User.objects.filter(username=username).count()

        context = R.ok().data('count', count)
        return http.JsonResponse(context)


# /mobiles/(?P<mobile>1[3-9]\d{9})/count/
class MobileCountView(View):
    """
    手机号重复注册
    """

    def get(self, request, mobile):
        """
        :param request:
        :param mobile: 手机号码
        :return: json
        """
        count = User.objects.filter(mobile=mobile).count()
        context = R.ok().data('count', count)
        return http.JsonResponse(context)


# /info
class UserInfoView(LoginRequiredMixin, View):
    """用户中心"""

    def get(self, request):
        """提供用户中心页面"""
        # 如果LoginRequiredMixin判断出用户已登录，那么request.user就是登陆用户对象
        context = {
            'username': request.user.username,
            'mobile': request.user.mobile,
            'email': request.user.email,
            'email_active': request.user.email_active
        }
        return render(request, HtmlTemplate.USER_CENTER_INFO_HTML, context)


# /emails/
class EmailView(LoginRequiredJSONMixin, View):
    """添加邮箱"""

    def put(self, request):
        """实现添加邮箱逻辑"""
        # 接收参数
        json_dict = json.loads(request.body.decode())
        email = json_dict.get('email')

        # 校验参数
        if not email:
            return http.HttpResponseForbidden('缺少email参数')
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return http.HttpResponseForbidden('参数email有误')

        # 赋值email字段

        request.user.email = email
        request.user.save()

        # 响应添加邮箱结果
        r = R.ok()
        r.errmsg = '添加邮箱成功'
        context = r.data()

        # 异步发送验证邮件
        verify_url = generate_verify_email_url(request.user)
        celery_send_verify_email.delay(email, verify_url)

        return http.JsonResponse(context)


# /emails/verification/
class VerifyEmailView(View):
    """验证邮箱"""

    def get(self, request):
        """实现邮箱验证逻辑"""
        # 接收参数
        token = request.GET.get('token')

        # 校验参数：判断token是否为空和过期，提取user
        if not token:
            return http.HttpResponseBadRequest('缺少token')

        user = check_verify_email_token(token)
        if not user:
            return http.HttpResponseForbidden('无效的token')

        # 修改email_active的值为True
        try:
            user.email_active = True
            user.save()
        except Exception as e:
            logger.error(e)
            return http.HttpResponseServerError('激活邮件失败')

        # 返回邮箱验证结果
        return redirect(reverse('users:info'))


# /addresses/
class AddressView(LoginRequiredMixin, View):
    """用户收货地址"""

    def get(self, request):
        """提供收货地址界面"""
        # 获取用户地址列表
        login_user = request.user
        addresses = Address.objects.filter(user=login_user, is_deleted=False)

        address_dict_list = []
        for address in addresses:
            address_dict = {
                "id": address.id,
                "title": address.title,
                "receiver": address.receiver,
                "province": address.province.name,
                "city": address.city.name,
                "district": address.district.name,
                "place": address.place,
                "mobile": address.mobile,
                "tel": address.tel,
                "email": address.email
            }
            address_dict_list.append(address_dict)

        context = {
            'default_address_id': login_user.default_address_id,
            'addresses': address_dict_list,
        }

        return render(request, HtmlTemplate.USER_CENTER_ADDRESS_HTML, context)


# /addresses/create/
class CreateAddressView(LoginRequiredJSONMixin, View):
    """新增地址视图"""

    def post(self, request):
        """实现新增地址逻辑"""
        # 判断是否超过地址上限：最多20个
        # Address.objects.filter(user=request.user).count()
        count = request.user.addresses.count()
        if count >= constants.USER_ADDRESS_COUNTS_LIMIT:
            r = R.set_result(StatusCodeEnum.THROTTLING_ERR)
            r.errmsg = '超过地址数量上限'
            context = r.data()
            return http.JsonResponse(context)

        # 接收参数
        json_dict = json.loads(request.body.decode())
        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')
        tel = json_dict.get('tel')
        email = json_dict.get('email')

        # 校验参数
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            raise BusinessException(StatusCodeEnum.NECESSARY_PARAM_ERR)
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            raise BusinessException(StatusCodeEnum.MOBILE_ERR)
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                raise BusinessException(StatusCodeEnum.TEL_ERR)
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                raise BusinessException(StatusCodeEnum.EMAIL_ERR)

        # 保存地址信息
        address = Address.objects.create(
            user=request.user,
            title=receiver,
            receiver=receiver,
            province_id=province_id,
            city_id=city_id,
            district_id=district_id,
            place=place,
            mobile=mobile,
            tel=tel,
            email=email
        )

        # 设置默认地址
        if not request.user.default_address:
            request.user.default_address = address
            request.user.save()

        # 新增地址成功，将新增的地址响应给前端实现局部刷新
        address_dict = {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }

        # 响应保存结果
        context = R.ok().data()
        context['address'] = address_dict
        return http.JsonResponse(context)


# /addresses/(?P<address_id>\d+)/
class UpdateDestroyAddressView(LoginRequiredJSONMixin, View):
    """修改和删除地址"""

    def put(self, request, address_id):
        """修改地址"""
        # 接收参数
        json_dict = json.loads(request.body.decode())
        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')
        tel = json_dict.get('tel')
        email = json_dict.get('email')

        # 校验参数
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            raise BusinessException(StatusCodeEnum.NECESSARY_PARAM_ERR)
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            raise BusinessException(StatusCodeEnum.MOBILE_ERR)
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                raise BusinessException(StatusCodeEnum.TEL_ERR)
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                raise BusinessException(StatusCodeEnum.EMAIL_ERR)

        # 判断地址是否存在,并更新地址信息
        Address.objects.filter(id=address_id).update(
            user=request.user,
            title=receiver,
            receiver=receiver,
            province_id=province_id,
            city_id=city_id,
            district_id=district_id,
            place=place,
            mobile=mobile,
            tel=tel,
            email=email
        )

        # 构造响应数据
        address = Address.objects.get(id=address_id)
        address_dict = {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }

        # 响应更新地址结果
        context = R.ok().data()
        context['address'] = address_dict
        return http.JsonResponse(context)

    def delete(self, request, address_id):
        """
        删除地址
        :param request: 请求对象
        :param address_id: 删除地址的id
        :return:
        """

        # 查询要删除的地址
        address = Address.objects.get(id=address_id)

        # 将地址逻辑删除设置为True
        address.is_deleted = True
        address.save()

        # 响应删除地址结果
        r = R.ok()
        r.errmsg = '删除地址成功'
        context = r.data()

        return http.JsonResponse(context)


# /addresses/(?P<address_id>\d+)/default/
class DefaultAddressView(LoginRequiredJSONMixin, View):
    """设置默认地址视图"""

    def put(self, request, address_id):
        """设置默认地址"""
        # 接收参数,查询地址
        address = Address.objects.get(id=address_id)

        # 设置地址为默认地址
        request.user.default_address = address
        request.user.save()

        # 响应设置默认地址结果
        context = R.ok().data()
        return http.JsonResponse(context)


# /addresses/(?P<address_id>\d+)/title/
class UpdateTitleAddressView(LoginRequiredJSONMixin, View):
    """设置地址标题"""

    def put(self, request, address_id):
        """设置地址标题"""
        # 接收参数：地址标题
        json_dict = json.loads(request.body.decode())
        title = json_dict.get('title')

        # 查询地址
        address = Address.objects.get(id=address_id)

        # 设置新的地址标题
        address.title = title
        address.save()

        # 响应删除地址结果
        context = R.ok().data()
        return http.JsonResponse(context)


# /password/
class ChangePasswordView(LoginRequiredMixin, View):
    """修改密码"""

    def get(self, request):
        """展示修改密码界面"""
        return render(request, HtmlTemplate.USER_CENTER_PASS_HTML)

    def post(self, request):
        """实现修改密码逻辑"""
        # 接收参数
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        new_password2 = request.POST.get('new_password2')

        # 校验参数
        if not all([old_password, new_password, new_password2]):
            raise BusinessException(StatusCodeEnum.NECESSARY_PARAM_ERR)

        result = request.user.check_password(old_password)
        if not result:
            return render(request, 'users/user_center_pass.html', {'origin_pwd_errmsg': '原始密码错误'})
        if not re.match(r'^[0-9A-Za-z]{8,20}$', new_password):
            raise BusinessException(StatusCodeEnum.PWD_ERR)
        if new_password != new_password2:
            raise BusinessException(StatusCodeEnum.CPWD_ERR)

        # 修改密码
        request.user.set_password(new_password)
        request.user.save()

        # 清理状态保持信息
        logout(request)
        response = redirect(reverse('users:login'))
        response.delete_cookie('username')

        # # 响应密码修改结果：重定向到登录界面
        return response


# /browse_histories/
class UserBrowseHistory(LoginRequiredJSONMixin, View):
    """用户浏览记录"""

    def get(self, request):
        """获取用户浏览记录"""
        # 获取Redis存储的sku_id列表信息
        redis_conn = get_redis_connection(settings.HISTORY_CACHE_ALIAS)
        user_id = request.user.id
        history_browse_key = RedisKey.HISTORY_BROWSE_KEY.format(user_id=user_id)
        sku_ids = redis_conn.lrange(history_browse_key, 0, -1)

        # 根据sku_ids列表数据，查询出商品sku信息
        skus = []
        for sku_id in sku_ids:
            sku = SKU.objects.get(id=sku_id)
            skus.append({
                'id': sku.id,
                'name': sku.name,
                'default_image_url': sku.default_image.url,
                'price': sku.price
            })

        context = R.ok().data()
        context['skus'] = skus
        return http.JsonResponse(context)

    def post(self, request):
        """保存用户浏览记录"""
        # 接收参数
        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get('sku_id')

        # 校验参数
        SKU.objects.get(id=sku_id)

        # 保存用户浏览数据
        redis_conn = get_redis_connection(settings.HISTORY_CACHE_ALIAS)
        pl = redis_conn.pipeline()
        user_id = request.user.id

        # sku商品历史浏览记录的 redis key
        history_browse_key = RedisKey.HISTORY_BROWSE_KEY.format(user_id=user_id)

        # 先去重
        pl.lrem(history_browse_key, 0, sku_id)
        # 再存储
        pl.lpush(history_browse_key, sku_id)
        # 最后截取
        pl.ltrim(history_browse_key, 0, 4)
        # 执行管道
        pl.execute()

        # 响应结果
        context = R.ok().data()
        return http.JsonResponse(context)
