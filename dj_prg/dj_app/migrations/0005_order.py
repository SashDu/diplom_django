# Generated by Django 4.2.1 on 2023-10-25 23:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dj_app', '0004_user_is_verified_email_emailverification'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=64, verbose_name='Фамилия')),
                ('email', models.EmailField(max_length=256, verbose_name='Почтовый ящик')),
                ('address', models.CharField(max_length=256, verbose_name='Адрес доставки')),
                ('basket_history', models.JSONField(default=dict, verbose_name='История корзины')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('status', models.SmallIntegerField(choices=[(0, 'Создан'), (1, 'Оплачен'), (2, 'В пути'), (3, 'Доставлен')], default=0, verbose_name='Статус')),
                ('initiator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Заказчик')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ['created'],
            },
        ),
    ]
