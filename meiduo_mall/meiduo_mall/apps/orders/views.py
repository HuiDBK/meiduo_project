import json
import logging
from decimal import Decimal

from django import http
from django.views import View
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.shortcuts import render
from django_redis import get_redis_connection

from orders import constants
from orders.models import OrderInfo
from orders.models import OrderGoods
from users.models import Address
from goods.models import SKU
from meiduo_mall.utils.result import R
from meiduo_mall.utils.constants import RedisKey
from meiduo_mall.utils.enums import StatusCodeEnum
from meiduo_mall.utils.constants import HtmlTemplate
from meiduo_mall.utils.views import LoginRequiredMixin
from meiduo_mall.utils.views import LoginRequiredJSONMixin
from meiduo_mall.utils.exceptions import BusinessException

logger = logging.getLogger(settings.LOGGER_NAME)


# /orders/settlement/
class OrderSettlementView(LoginRequiredMixin, View):
    """结算订单"""

    def get(self, request):
        """提供订单结算页面"""
        # 获取登录用户
        user = request.user

        # 查询地址信息
        try:
            addresses = Address.objects.filter(user=request.user, is_deleted=False)
        except Address.DoesNotExist:
            # 如果地址为空，渲染模板时会判断，并跳转到地址编辑页面
            addresses = None

        # 从Redis购物车中查询出被勾选的商品信息
        redis_conn = get_redis_connection(settings.CARTS_CACHE_ALIAS)

        user_carts_key = RedisKey.USER_CARTS_KEY.format(user_id=user.id)
        carts_selected_key = RedisKey.CARTS_SELECTED_KEY.format(user_id=user.id)

        redis_cart = redis_conn.hgetall(user_carts_key)
        cart_selected = redis_conn.smembers(carts_selected_key)

        cart = {}
        for sku_id in cart_selected:
            cart[int(sku_id)] = int(redis_cart[sku_id])

        # 准备初始值
        total_count = 0
        total_amount = Decimal(0.00)

        # 查询商品信息
        skus = SKU.objects.filter(id__in=cart.keys())
        for sku in skus:
            sku.count = cart[sku.id]
            sku.amount = sku.count * sku.price

            # 计算总数量和总金额
            total_count += sku.count
            total_amount += sku.count * sku.price

        # 补充运费
        freight = Decimal(constants.ORDER_FREIGHT)

        # 渲染界面
        context = {
            'addresses': addresses,
            'skus': skus,
            'total_count': total_count,
            'total_amount': total_amount,
            'freight': freight,
            'payment_amount': total_amount + freight
        }

        return render(request, HtmlTemplate.ORDER_PLACE_HTML, context)


# /orders/commit/
class OrderCommitView(LoginRequiredJSONMixin, View):
    """订单提交"""

    def save_order(self, user, order_id, address, pay_method):

        # 保存订单基本信息（一）
        if pay_method == OrderInfo.PAY_METHODS_ENUM['ALIPAY']:
            pay_status = OrderInfo.ORDER_STATUS_ENUM['UNPAID']
        else:
            pay_status = OrderInfo.ORDER_STATUS_ENUM['UNSEND']

        order = OrderInfo.objects.create(
            order_id=order_id,
            user=user,
            address=address,
            total_count=0,
            total_amount=Decimal(0.00),
            freight=Decimal(10.00),
            pay_method=pay_method,
            # status = 'UNPAID' if pay_method=='ALIPAY' else 'UNSEND'
            status=pay_status
        )

        # 保存订单商品信息（多）

        # 查询redis购物车中被勾选的商品
        redis_conn = get_redis_connection(settings.CARTS_CACHE_ALIAS)
        user_carts_key = RedisKey.USER_CARTS_KEY.format(user_id=user.id)
        carts_selected_key = RedisKey.CARTS_SELECTED_KEY.format(user_id=user.id)

        # 所有的购物车数据，包含了勾选和未勾选 ：{b'1': b'1', b'2': b'2'}
        redis_cart = redis_conn.hgetall(user_carts_key)

        # 被勾选的商品的sku_id：[b'1']
        redis_selected = redis_conn.smembers(carts_selected_key)

        # 构造购物车中被勾选的商品的数据 {b'1': b'1'}
        new_cart_dict = {}
        for sku_id in redis_selected:
            new_cart_dict[int(sku_id)] = int(redis_cart[sku_id])

        # 获取被勾选的商品的sku_id
        sku_ids = new_cart_dict.keys()
        for sku_id in sku_ids:

            # 每个商品都有多次下单的机会，直到库存不足
            while True:
                # 读取购物车商品信息
                sku = SKU.objects.get(id=sku_id)  # 查询商品和库存信息时，不能出现缓存，所以没用filter(id__in=sku_ids)

                # 获取原始的库存和销量
                origin_stock = sku.stock
                origin_sales = sku.sales

                # 获取要提交订单的商品的数量
                sku_count = new_cart_dict[sku.id]

                # 判断商品数量是否大于库存，如果大于，响应"库存不足"
                if sku_count > origin_stock:
                    # 库存不足，抛异常回滚事务
                    raise BusinessException(StatusCodeEnum.STOCK_ERR)

                # 模拟网络延迟
                # import time
                # time.sleep(7)

                # SKU 减库存，加销量
                # sku.stock -= sku_count
                # sku.sales += sku_count
                # sku.save()

                new_stock = origin_stock - sku_count
                new_sales = origin_sales + sku_count
                result = SKU.objects.filter(id=sku_id, stock=origin_stock).update(stock=new_stock, sales=new_sales)

                # 如果在更新数据时，原始数据变化了，返回0；表示有资源抢夺
                if result == 0:
                    # 库存 10，要买1，但是在下单时，有资源抢夺，被买走1，剩下9个，如果库存依然满足，继续下单，直到库存不足为止
                    continue

                # SPU 加销量
                sku.spu.sales += sku_count
                sku.spu.save()

                OrderGoods.objects.create(
                    order=order,
                    sku=sku,
                    count=sku_count,
                    price=sku.price,
                )

                # 累加订单商品的数量和总价到订单基本信息表
                order.total_count += sku_count
                order.total_amount += sku_count * sku.price

                # 下单成功，记得break
                break

        # 再加最后的运费
        order.total_amount += order.freight
        order.save()

        # 下单成功, 清除购物车中已结算的商品
        pl = redis_conn.pipeline()
        pl.hdel(user_carts_key, *redis_selected)
        pl.srem(carts_selected_key, *redis_selected)
        pl.execute()

    def post(self, request):
        """保存订单信息和订单商品信息"""
        # 获取当前要保存的订单数据
        json_dict = json.loads(request.body.decode())
        address_id = json_dict.get('address_id')
        pay_method = json_dict.get('pay_method')

        # 校验参数
        if not all([address_id, pay_method]):
            return http.HttpResponseForbidden('缺少必传参数')

        # 判断address_id是否合法
        try:
            address = Address.objects.get(id=address_id)
        except Exception:
            return http.HttpResponseForbidden('参数address_id错误')

        # 判断pay_method是否合法
        if pay_method not in [OrderInfo.PAY_METHODS_ENUM['CASH'], OrderInfo.PAY_METHODS_ENUM['ALIPAY']]:
            return http.HttpResponseForbidden('参数pay_method错误')

        # 获取登录用户
        user = request.user
        # 生成订单编号：年月日时分秒+用户编号
        order_id = timezone.localtime().strftime('%Y%m%d%H%M%S') + ('%09d' % user.id)

        # 显式的开启一个事务
        with transaction.atomic():
            # 创建事务保存点
            save_id = transaction.savepoint()

            try:
                # 保存订单
                self.save_order(user, order_id, address, pay_method)
            except Exception as e:
                # 保存订单发生异常 回滚事务
                logger.error(e)
                transaction.savepoint_rollback(save_id)
                context = R.set_result(StatusCodeEnum.DB_ERR).data()
                return http.JsonResponse(context)

            # 数据库操作成功，明显的提交一次事务
            transaction.savepoint_commit(save_id)

        # 响应提交订单结果
        context = R.ok().data()
        context['order_id'] = order_id
        return http.JsonResponse(context)


# /orders/success/
class OrderSuccessView(LoginRequiredMixin, View):
    """提交订单成功"""

    def get(self, request):
        order_id = request.GET.get('order_id')
        payment_amount = request.GET.get('payment_amount')
        pay_method = request.GET.get('pay_method')

        context = {
            'order_id': order_id,
            'payment_amount': payment_amount,
            'pay_method': pay_method
        }
        return render(request, HtmlTemplate.ORDER_SUCCESS_HTML, context)
