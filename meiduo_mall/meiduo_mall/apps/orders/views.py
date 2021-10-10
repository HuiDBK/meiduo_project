from decimal import Decimal

from django.shortcuts import render
from django.views import View
from django.conf import settings
from django_redis import get_redis_connection

from orders import constants
from users.models import Address
from goods.models import SKU
from meiduo_mall.utils.constants import RedisKey
from meiduo_mall.utils.constants import HtmlTemplate
from meiduo_mall.utils.views import LoginRequiredMixin


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
