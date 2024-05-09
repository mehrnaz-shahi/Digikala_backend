from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from products.models import Product
from retailers.models import Retailer

User = get_user_model()


class ProductRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'product')
        verbose_name = "Product Rating"
        verbose_name_plural = "Product Ratings"

    def __str__(self):
        return f"{self.user.phone_number} - {self.product.name} - {self.rating}"


class RetailerRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='retailer_ratings')
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'retailer')
        verbose_name = "Retailer Rating"
        verbose_name_plural = "Retailer Ratings"

    def __str__(self):
        return f"{self.user.phone_number} - {self.retailer.name} - {self.rating}"
