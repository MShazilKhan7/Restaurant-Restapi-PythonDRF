# Generated by Django 4.2 on 2023-04-10 20:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0008_menuitem_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='API.category'),
        ),
    ]