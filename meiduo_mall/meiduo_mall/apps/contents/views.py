from django.views import View
from django.shortcuts import render


# /
class IndexView(View):
    """商城首页类视图"""

    def get(self, request):
        return render(request, 'index.html')