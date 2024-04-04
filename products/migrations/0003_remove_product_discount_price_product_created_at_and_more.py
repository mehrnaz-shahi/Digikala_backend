# Generated by Django 5.0.3 on 2024-04-01 14:48

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_discount_price_product_is_discounted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='discount_price',
        ),
        migrations.AddField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='product',
            name='discount_percentage',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]