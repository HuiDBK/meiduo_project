# Generated by Django 3.2.7 on 2021-09-30 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210929_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_active',
            field=models.BooleanField(default=False, verbose_name='邮箱验证状态'),
        ),
    ]
