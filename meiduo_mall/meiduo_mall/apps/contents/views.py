from django.views import View
from django.shortcuts import render
from contents.utils import get_categories
from contents.models import ContentCategory

from meiduo_mall.utils.constants import HtmlTemplate


# /
class IndexView(View):
    """商城首页类视图"""

    def get(self, request):
        # 查询商品频道和分类
        categories = get_categories()

        # 广告数据
        contents = {}
        content_categories = ContentCategory.objects.all()
        for cat in content_categories:
            contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

        # 渲染模板的上下文
        context = {
            'categories': categories,
            'contents': contents,
        }
        return render(request, HtmlTemplate.INDEX_HTML, context)
