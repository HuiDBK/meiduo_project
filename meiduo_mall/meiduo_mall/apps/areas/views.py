from django.shortcuts import render
from django.views import View
from django.core.cache import cache
from django.http import JsonResponse

from areas.models import Area
from meiduo_mall.utils.result import R
from meiduo_mall.utils.constants import RedisKey


# /areas/
class AreasView(View):
    """省市区数据"""

    def get(self, request):
        """提供省市区数据"""
        area_id = request.GET.get('area_id')

        if not area_id:
            # 读取省份缓存数据
            provinces_key = RedisKey.PROVINCES_KEY
            province_list = cache.get(provinces_key)

            if not province_list:
                # 查询省份数据
                province_model_list = Area.objects.filter(parent__isnull=True)
                # 序列化省级数据
                province_list = []
                for province_model in province_model_list:
                    province_list.append({'id': province_model.id, 'name': province_model.name})

                # 缓存省份字典列表数据:默认存储到别名为"default"的配置中
                cache.set(provinces_key, province_list, 3600)

            # 响应省份数据
            context = R.ok().data()
            context['province_list'] = province_list

            return JsonResponse(context)
        else:

            # 读取市或区缓存数据
            sub_area_key = RedisKey.SUB_AREA_KEY.format(area_id=area_id)
            sub_data = cache.get(sub_area_key)

            if not sub_data:

                # 提供市或区数据
                parent_model = Area.objects.get(id=area_id)  # 查询市或区的父级
                sub_model_list = parent_model.subs.all()

                # 序列化市或区数据
                sub_list = []
                for sub_model in sub_model_list:
                    sub_list.append({'id': sub_model.id, 'name': sub_model.name})

                sub_data = {
                    'id': parent_model.id,  # 父级pk
                    'name': parent_model.name,  # 父级name
                    'subs': sub_list  # 父级的子集
                }

                # 储存市或区缓存数据
                cache.set(sub_area_key, sub_data, 3600)

            # 响应市或区数据
            context = R.ok().data()
            context['sub_data'] = sub_data
            return JsonResponse(context)
