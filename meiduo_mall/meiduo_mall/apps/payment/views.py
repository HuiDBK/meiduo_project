from django import http
from django.views import View
from django.conf import settings
from django.shortcuts import render

from alipay import AliPay
from payment.models import Payment
from orders.models import OrderInfo
from meiduo_mall.utils.result import R
from meiduo_mall.utils.constants import HtmlTemplate
from meiduo_mall.utils.views import LoginRequiredJSONMixin


def create_alipay():
    """
    创建 alipay 支付对象
    :return: alipay
    """

    # 读取应用私钥, 阿里支付公钥文件数据
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
    return alipay


# 测试账号：irhkhm7606@sandbox.com
# /payment/(?P<order_id>\d+)/
class PaymentView(LoginRequiredJSONMixin, View):
    """订单支付功能"""

    def get(self, request, order_id):
        """
        :param request: 当前请求对象
        :param order_id: 当前要支付的订单ID
        :return: JSON
        """
        # 查询要支付的订单
        user = request.user
        order = OrderInfo.objects.get(order_id=order_id, user=user, status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'])

        # 创建支付宝支付对象
        alipay = create_alipay()

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


# /payment/status/
class PaymentStatusView(View):
    """保存订单支付结果"""

    def get(self, request):
        # 获取前端传入的请求参数
        query_dict = request.GET
        data = query_dict.dict()

        # 获取并从请求参数中剔除signature
        signature = data.pop('sign')

        alipay = create_alipay()

        # 校验这个重定向是否是alipay重定向过来的
        success = alipay.verify(data, signature)

        if success:
            # 读取order_id
            order_id = data.get('out_trade_no')

            # 读取支付宝流水号
            trade_id = data.get('trade_no')

            # 保存Payment模型类数据
            Payment.objects.create(
                order_id=order_id,
                trade_id=trade_id
            )

            # 修改订单状态为待评价
            OrderInfo.objects.filter(order_id=order_id, status=OrderInfo.ORDER_STATUS_ENUM['UNPAID']).update(
                status=OrderInfo.ORDER_STATUS_ENUM["UNCOMMENT"])

            # 响应trade_id
            context = {
                'trade_id': trade_id
            }
            return render(request, HtmlTemplate.PAY_SUCCESS_HTML, context)
        else:
            # 订单支付失败，重定向到我的订单
            return http.HttpResponseForbidden('非法请求')
