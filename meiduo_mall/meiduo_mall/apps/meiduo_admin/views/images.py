from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from goods.models import SKUImage, SKU
from meiduo_admin.serializers.images import ImagesSerializer, SKUSerializer
from meiduo_admin.utils import PageNum
from rest_framework.permissions import IsAdminUser


class ImagesView(ModelViewSet):
    queryset = SKUImage.objects.all()
    serializer_class = ImagesSerializer
    pagination_class = PageNum
    permission_classes = [IsAdminUser]

    def simple(self, request):
        """
        获取sku商品信息
        :param request:
        :return:
        """
        # 1、查询所有sku商品
        skus = SKU.objects.all()
        # 2、序列化返回
        ser = SKUSerializer(skus, many=True)
        return Response(ser.data)
