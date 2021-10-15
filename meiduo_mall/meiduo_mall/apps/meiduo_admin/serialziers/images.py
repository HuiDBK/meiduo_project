from django.conf import settings
from fdfs_client.client import Fdfs_client, get_tracker_conf
from rest_framework import serializers
from goods.models import SKUImage, SKU
from celery_tasks.static_file.tasks import get_detail_html


def create_fdfs_client():
    """
    创建 FastDFS 客户端
    :return:
    """
    client_conf = get_tracker_conf(settings.FASTDFS_PATH)
    fdfs_client = Fdfs_client(client_conf)
    return fdfs_client


class ImagesSerializer(serializers.ModelSerializer):
    """
    图片序列化器
    """

    class Meta:
        model = SKUImage
        fields = "__all__"

    def create(self, validated_data):
        # 3、建立fastdfs的客户端
        client = create_fdfs_client
        # self.context['request'] 获取request对象

        file = self.context['request'].FILES.get('image')
        # 4、上传图片
        res = client.upload_by_buffer(file.read())
        # 5、判断是否上传成功
        if res['Status'] != 'Upload successed.':
            raise serializers.ValidationError({'error': '图片上传失败'})

        # 6、保存图片表
        img = SKUImage.objects.create(sku=validated_data['sku'], image=res['Remote file_id'])

        # 异步生成详情页静态页面
        get_detail_html.delay(img.sku.id)

        return img

    def update(self, instance, validated_data):
        # 3、建立fastdfs的客户端
        client = create_fdfs_client()

        # self.context['request'] 获取request对象

        file = self.context['request'].FILES.get('image')
        # 4、上传图片
        res = client.upload_by_buffer(file.read())
        # 5、判断是否上传成功
        if res['Status'] != 'Upload successed.':
            raise serializers.ValidationError({'error': '图片上传失败'})

        # 6、更新图片表
        instance.image = res['Remote file_id'].decode()
        instance.save()

        # 异步生成详情页静态页面
        get_detail_html.delay(instance.sku.id)
        return instance


class SKUSerializer(serializers.ModelSerializer):
    """
        sku序列化器
    """

    class Meta:
        model = SKU
        fields = ('id', 'name')
