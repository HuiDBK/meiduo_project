import json
import pickle
import base64

from django import http
from django.views import View
from django.conf import settings
from django.shortcuts import render
from django_redis import get_redis_connection
from goods.models import SKU
from carts import constants

from meiduo_mall.utils.result import R
from meiduo_mall.utils.constants import RedisKey
from meiduo_mall.utils.constants import CookieKey
from meiduo_mall.utils.constants import HtmlTemplate


# /carts/
class CartsView(View):
    """购物车管理"""

    def get(self, request):
        """展示购物车"""
        user = request.user
        if user.is_authenticated:

            # 用户已登录，查询redis购物车
            redis_conn = get_redis_connection(settings.CARTS_CACHE_ALIAS)

            # 获取redis中的购物车数据
            user_carts_key = RedisKey.USER_CARTS_KEY.format(user_id=user.id)
            redis_cart = redis_conn.hgetall(user_carts_key)

            # 获取redis中的选中状态
            carts_selected_key = RedisKey.CARTS_SELECTED_KEY.format(user_id=user.id)
            cart_selected = redis_conn.smembers(carts_selected_key)

            # 将redis中的数据构造成跟cookie中的格式一致，方便统一查询
            cart_dict = {}
            for sku_id, count in redis_cart.items():
                cart_dict[int(sku_id)] = {
                    'count': int(count),
                    'selected': sku_id in cart_selected
                }
        else:
            # 用户未登录，查询cookies购物车
            carts_str = request.COOKIES.get(CookieKey.CARTS_KEY)
            if carts_str:
                # 将cart_str转成bytes,再将bytes转成base64的bytes,最后将bytes转字典
                cart_dict = pickle.loads(base64.b64decode(carts_str.encode()))
            else:
                cart_dict = {}

        # 构造购物车渲染数据
        sku_ids = cart_dict.keys()
        skus = SKU.objects.filter(id__in=sku_ids)
        cart_skus = []
        for sku in skus:
            cart_skus.append({
                'id': sku.id,
                'name': sku.name,
                'count': cart_dict.get(sku.id).get('count'),
                'selected': str(cart_dict.get(sku.id).get('selected')),  # 将True，转'True'，方便json解析
                'default_image_url': sku.default_image.url,
                'price': str(sku.price),  # 从Decimal('10.2')中取出'10.2'，方便json解析
                'amount': str(sku.price * cart_dict.get(sku.id).get('count')),
            })

        context = {
            'cart_skus': cart_skus,
        }

        # 渲染购物车页面
        return render(request, HtmlTemplate.CART_LIST_HTML, context)

    def post(self, request):
        """添加购物车"""
        # 接收参数
        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get('sku_id')
        count = json_dict.get('count')
        selected = json_dict.get('selected', True)

        # 判断参数是否齐全
        if not all([sku_id, count]):
            return http.HttpResponseForbidden('缺少必传参数')

        # 判断sku_id是否存在
        try:
            SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return http.HttpResponseForbidden('商品不存在')

        # 判断count是否为数字
        try:
            count = int(count)
        except Exception:
            return http.HttpResponseForbidden('参数count有误')

        # 判断selected是否为bool值
        if selected:
            if not isinstance(selected, bool):
                return http.HttpResponseForbidden('参数selected有误')

        # 判断用户是否登录
        user = request.user
        if user.is_authenticated:
            # 用户已登录，操作redis购物车
            redis_conn = get_redis_connection(settings.CARTS_CACHE_ALIAS)
            pl = redis_conn.pipeline()

            user_carts_key = RedisKey.USER_CARTS_KEY.format(user_id=user.id)
            # 新增购物车数据
            pl.hincrby(user_carts_key, sku_id, count)

            # 新增选中的状态
            if selected:
                carts_selected_key = RedisKey.CARTS_SELECTED_KEY.format(user_id=user.id)
                pl.sadd(carts_selected_key, sku_id)

            # 执行管道
            pl.execute()

            # 响应结果
            context = R.ok().data()
            return http.JsonResponse(context)
        else:
            # 用户未登录，操作cookie购物车
            cart_str = request.COOKIES.get(CookieKey.CARTS_KEY)

            # 如果用户操作过cookie购物车
            if cart_str:
                # 将cart_str转成bytes,再将bytes转成base64的bytes,最后将bytes转字典
                cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
            else:  # 用户从没有操作过cookie购物车
                cart_dict = {}

            # 判断要加入购物车的商品是否已经在购物车中,如有相同商品，累加求和，反之，直接赋值
            if sku_id in cart_dict:
                # 累加求和
                origin_count = cart_dict[sku_id]['count']
                count += origin_count

            cart_dict[sku_id] = {
                'count': count,
                'selected': selected
            }

            # 将字典转成bytes,再将bytes转成base64的bytes,最后将bytes转字符串
            cookie_cart_str = base64.b64encode(pickle.dumps(cart_dict)).decode()

            # 创建响应对象
            context = R.ok().data()
            response = http.JsonResponse(context)

            # 响应结果并将购物车数据写入到cookie
            response.set_cookie(CookieKey.CARTS_KEY, cookie_cart_str, max_age=constants.CARTS_COOKIE_EXPIRES)
            return response

    def put(self, request):
        """修改购物车"""
        # 接收参数
        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get('sku_id')
        count = json_dict.get('count')
        selected = json_dict.get('selected', True)

        # 判断参数是否齐全
        if not all([sku_id, count]):
            return http.HttpResponseForbidden('缺少必传参数')

        # 判断sku_id是否存在
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return http.HttpResponseForbidden('商品sku_id不存在')

        # 判断count是否为数字
        try:
            count = int(count)
        except Exception:
            return http.HttpResponseForbidden('参数count有误')

        # 判断selected是否为bool值
        if selected:
            if not isinstance(selected, bool):
                return http.HttpResponseForbidden('参数selected有误')

        # 判断用户是否登录
        user = request.user
        if user.is_authenticated:
            # 用户已登录，修改redis购物车
            redis_conn = get_redis_connection(settings.CARTS_CACHE_ALIAS)
            pl = redis_conn.pipeline()

            # 因为接口设计为幂等的，直接覆盖
            user_carts_key = RedisKey.USER_CARTS_KEY.format(user_id=user.id)
            pl.hset(user_carts_key, sku_id, count)

            # 是否选中
            carts_selected_key = RedisKey.CARTS_SELECTED_KEY.format(user_id=user.id)
            if selected:
                pl.sadd(carts_selected_key, sku_id)
            else:
                pl.srem(carts_selected_key, sku_id)
            pl.execute()

            # 创建响应对象
            cart_sku = {
                'id': sku_id,
                'count': count,
                'selected': selected,
                'name': sku.name,
                'default_image_url': sku.default_image.url,
                'price': sku.price,
                'amount': sku.price * count,
            }
            context = R.ok().data()
            context['cart_sku'] = cart_sku
            return http.JsonResponse(context)
        else:
            # 用户未登录，修改cookie购物车
            cart_str = request.COOKIES.get(CookieKey.CARTS_KEY)
            if cart_str:
                # 将cart_str转成bytes,再将bytes转成base64的bytes,最后将bytes转字典
                cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
            else:
                cart_dict = {}

            # 因为接口设计为幂等的，直接覆盖
            cart_dict[sku_id] = {
                'count': count,
                'selected': selected
            }

            # 将字典转成bytes,再将bytes转成base64的bytes,最后将bytes转字符串
            cookie_cart_str = base64.b64encode(pickle.dumps(cart_dict)).decode()

            # 创建响应对象
            cart_sku = {
                'id': sku_id,
                'count': count,
                'selected': selected,
                'name': sku.name,
                'default_image_url': sku.default_image.url,
                'price': sku.price,
                'amount': sku.price * count,
            }

            context = R.ok().data()
            context['cart_sku'] = cart_sku
            response = http.JsonResponse(context)

            # 响应结果并将购物车数据写入到cookie
            response.set_cookie(CookieKey.CARTS_KEY, cookie_cart_str, max_age=constants.CARTS_COOKIE_EXPIRES)
            return response

    def delete(self, request):
        """删除购物车"""
        # 接收参数
        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get('sku_id')

        # 判断sku_id是否存在
        try:
            SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return http.HttpResponseForbidden('商品不存在')

        # 判断用户是否登录
        user = request.user
        if user is not None and user.is_authenticated:
            # 用户未登录，删除redis购物车
            redis_conn = get_redis_connection(settings.CARTS_CACHE_ALIAS)
            pl = redis_conn.pipeline()

            # 删除键，就等价于删除了整条记录
            user_carts_key = RedisKey.USER_CARTS_KEY.format(user_id=user.id)
            carts_selected_key = RedisKey.CARTS_SELECTED_KEY.format(user_id=user.id)
            pl.hdel(user_carts_key, sku_id)
            pl.srem(carts_selected_key, sku_id)
            pl.execute()

            # 删除结束后，没有响应的数据，只需要响应状态码即可
            context = R.ok().data()
            return http.JsonResponse(context)
        else:
            # 用户未登录，删除cookie购物车
            cart_str = request.COOKIES.get(CookieKey.CARTS_KEY)
            if cart_str:
                # 将cart_str转成bytes,再将bytes转成base64的bytes,最后将bytes转字典
                cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
            else:
                cart_dict = {}

            # 创建响应对象
            context = R.ok().data()
            response = http.JsonResponse(context)

            if sku_id in cart_dict:
                del cart_dict[sku_id]
                # 将字典转成bytes,再将bytes转成base64的bytes,最后将bytes转字符串
                cookie_cart_str = base64.b64encode(pickle.dumps(cart_dict)).decode()
                # 响应结果并将购物车数据写入到cookie
                response.set_cookie(CookieKey.CARTS_KEY, cookie_cart_str, max_age=constants.CARTS_COOKIE_EXPIRES)
            return response


# /carts/selection/
class CartsSelectAllView(View):
    """全选购物车"""

    def put(self, request):
        # 接收参数
        json_dict = json.loads(request.body.decode())
        selected = json_dict.get('selected', True)

        # 校验参数
        if selected:
            if not isinstance(selected, bool):
                return http.HttpResponseForbidden('参数selected有误')

        # 判断用户是否登录
        user = request.user
        if user is not None and user.is_authenticated:
            # 用户已登录，操作redis购物车
            redis_conn = get_redis_connection(settings.CARTS_CACHE_ALIAS)

            user_carts_key = RedisKey.USER_CARTS_KEY.format(user_id=user.id)
            cart = redis_conn.hgetall(user_carts_key)

            carts_selected_key = RedisKey.CARTS_SELECTED_KEY.format(user_id=user.id)
            sku_id_list = cart.keys()
            if selected:
                # 全选
                redis_conn.sadd(carts_selected_key, *sku_id_list)
            else:
                # 取消全选
                redis_conn.srem(carts_selected_key, *sku_id_list)

            context = R.ok().data()
            return http.JsonResponse(context)
        else:
            # 用户已登录，操作cookie购物车
            cart = request.COOKIES.get(CookieKey.CARTS_KEY)
            context = R.ok().data()
            response = http.JsonResponse(context)
            if cart is not None:
                cart = pickle.loads(base64.b64decode(cart.encode()))
                for sku_id in cart:
                    cart[sku_id]['selected'] = selected
                cookie_cart = base64.b64encode(pickle.dumps(cart)).decode()
                response.set_cookie(CookieKey.CARTS_KEY, cookie_cart, max_age=constants.CARTS_COOKIE_EXPIRES)

            return response
