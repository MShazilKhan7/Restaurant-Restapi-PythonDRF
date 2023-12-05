# Generated by Django 4.2 on 2023-04-13 07:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('API', '0015_alter_cart_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='price',
            new_name='total',
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterUniqueTogether(
            name='orderitem',
            unique_together={('order', 'menu_item')},
        ),
    ]
