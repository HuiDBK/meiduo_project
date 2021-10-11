from django import http
from django.views import View
from django.conf import settings

from alipay import AliPay
from orders.models import OrderInfo
from meiduo_mall.utils.result import R
from meiduo_mall.utils.views import LoginRequiredJSONMixin


# 测试账号：irhkhm7606@sandbox.com
# /payment/(?P<order_id>\d+)/
class PaymentView(LoginRequiredJSONMixin, View):
    """订单支付功能"""

    def get(self, request, order_id):
        # 查询要支付的订单
        user = request.user
        order = OrderInfo.objects.get(order_id=order_id, user=user, status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'])

        with open(settings.ALIPAY_PUBLIC_KEY_PATH, mode='r') as f:
            alipay_public_key_str = f.read()

        with open(settings.APP_PRIVATE_KEY_PATH, mode='r') as f:
            app_private_key_str = f.read()

        # 创建支付宝支付对象
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调url
            alipay_public_key_string=alipay_public_key_str,
            app_private_key_string=app_private_key_str,
            sign_type="RSA2",
            debug=settings.ALIPAY_DEBUG
        )

        # 生成登录支付宝链接
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=str(order.total_amount),
            subject="美多商城%s" % order_id,
            return_url=settings.ALIPAY_RETURN_URL,
        )

        # 响应登录支付宝连接
        # 真实环境电脑网站支付网关：https://openapi.alipay.com/gateway.do? + order_string
        # 沙箱环境电脑网站支付网关：https://openapi.alipaydev.com/gateway.do? + order_string
        alipay_url = settings.ALIPAY_URL + "?" + order_string
        context = R.ok().data()
        context['alipay_url'] = alipay_url
        return http.JsonResponse(context)


