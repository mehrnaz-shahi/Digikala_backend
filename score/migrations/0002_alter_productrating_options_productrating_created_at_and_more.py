# Generated by Django 5.0.3 on 2024-04-01 14:48

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retailers', '0002_alter_retailer_contact_number'),
        ('score', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productrating',
            options={'verbose_name': 'Product Rating', 'verbose_name_plural': 'Product Ratings'},
        ),
        migrations.AddField(
            model_name='productrating',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='productrating',
            name='rating',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.CreateModel(
            name='RetailerRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('retailer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='retailers.retailer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='retailer_ratings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Retailer Rating',
                'verbose_name_plural': 'Retailer Ratings',
                'unique_together': {('user', 'retailer')},
            },
        ),
    ]