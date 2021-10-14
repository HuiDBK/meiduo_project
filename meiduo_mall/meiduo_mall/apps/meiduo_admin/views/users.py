from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView

from meiduo_admin.serialziers.users import UserSerialzier
from meiduo_admin.utils import UserPageNum
from users.models import User


# /users/
class UserView(ListCreateAPIView):
    """
    获取用户数据
    """

    # 指定序列化器
    serializer_class = UserSerialzier
    # 使用分页器
    pagination_class = UserPageNum

    # 重写获取查询集数据的方法
    def get_queryset(self):
        key_word = self.request.query_params.get('keyword')
        if key_word == '':
            return User.objects.all()
        else:
            return User.objects.filter(username__contains=key_word)
