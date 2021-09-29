from django.db import models
from meiduo_mall.utils.models import BaseModel


class OAuthGiteeUser(BaseModel):
    """QQ登录用户数据"""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='用户')
    gitee_uid = models.CharField(max_length=64, verbose_name='gitee 用户id', db_index=True)

    class Meta:
        db_table = 'meiduo_oauth_gitee'
        verbose_name = 'Gitee登录用户数据'
        verbose_name_plural = verbose_name
