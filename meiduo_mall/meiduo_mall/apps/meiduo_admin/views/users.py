from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView

from meiduo_admin.serialziers.users import UserSerializer
from meiduo_admin.serialziers.users import UserAddSerializer
from meiduo_admin.utils import PageNum
from users.models import User


# /users/
class UserView(ListCreateAPIView):
    """
    获取用户数据
    """

    # 指定序列化器
    serializer_class = UserSerializer

    # 使用分页器
    pagination_class = PageNum

    # 根据不同的请求方式返回不同序列化器
    def get_serializer_class(self):
        # 请求方式是GET，则是获取用户数据返回UserSerializer
        if self.request.method == 'GET':
            return UserSerializer
        else:
            # POST请求，完成保存用户，返回UserAddSerializer
            return UserAddSerializer

    # 重写获取查询集数据的方法
    def get_queryset(self):
        key_word = self.request.query_params.get('keyword')
        if key_word == '':
            return User.objects.all()
        else:
            return User.objects.filter(username__contains=key_word)
