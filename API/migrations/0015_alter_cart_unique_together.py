# Generated by Django 4.2 on 2023-04-11 14:37

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('API', '0014_orderitem_order_cart'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cart',
            unique_together={('menu_item', 'user')},
        ),
    ]
