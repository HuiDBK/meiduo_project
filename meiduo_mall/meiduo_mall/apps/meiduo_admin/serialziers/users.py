import re

from users.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化器
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'mobile', 'email', 'password')  # id 默认read_only
        extra_kwargs = {
            'password': {
                'write_only': True,
                'max_length': 20,
                'min_length': 8,
            },

            'username': {
                'max_length': 20,
                'min_length': 5,
            },

        }

    def validate_mobile(self, value):
        if not re.match(r'1[3-9]\d{9}', value):
            raise serializers.ValidationError('手机格式不对')
        return value

    def create(self, validated_data):
        # user = super().create(validated_data)
        # 密码加密
        # user.set_password(validated_data['password'])
        # user.save()

        user = User.objects.create_user(**validated_data)
        return user


class UserAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'mobile', 'email', 'password')
        # username字段增加长度限制，password字段只参与保存，不在返回给前端，增加write_only选项参数
        extra_kwargs = {
            'username': {
                'max_length': 20,
                'min_length': 5
            },
            'password': {
                'max_length': 20,
                'min_length': 8,
                'write_only': True

            },
        }

    # 重写create方法
    def create(self, validated_data):
        # 保存用户数据并对密码加密
        user = User.objects.create_user(**validated_data)
        return user
