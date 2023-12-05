# Generated by Django 4.2 on 2023-04-13 15:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('API', '0016_rename_price_order_total_alter_order_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='menu_item',
            new_name='menuitem',
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_crew',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='delivery_crew', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='orderitem',
            unique_together={('order', 'menuitem')},
        ),
    ]
