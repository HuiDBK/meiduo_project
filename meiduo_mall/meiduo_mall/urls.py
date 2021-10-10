from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # 用户模块路由
    url(r'^', include(('users.urls', 'users'), namespace='users')),

    # 商城首页广告内容模块路由
    url(r'^', include(('contents.urls', 'contents'), namespace='contents')),

    # 验证码校验模块路由
    url(r'^', include(('verifications.urls', 'verifications'), namespace='verifications')),

    # oauth 登录认证模块
    url(r'^', include(('oauth.urls', 'oauth'), namespace='oauth')),

    # 省市区三级联动模块
    url(r'^', include(('areas.urls', 'areas'), namespace='areas')),

    # 商品模块路由
    url(r'^', include(('goods.urls', 'goods'), namespace='goods')),

    # 全文检索路由
    url(r'^search/', include('haystack.urls')),

    # 购物车模块路由
    url(r'^', include(('carts.urls', 'carts'), namespace='carts')),

    # 订单模块路由
    url(r'^', include(('orders.urls', 'orders'), namespace='orders')),
]
