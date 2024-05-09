from django.utils import timezone
from django.db import models
from django.db.models import Avg
from retailers.models import Retailer


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='subcategories')

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_discounted = models.BooleanField(default=False)  # Field for discount status
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    discount_time = models.DateTimeField(null=True, blank=True)

    categories = models.ManyToManyField(Category, related_name='products', blank=True)

    colors = models.ManyToManyField(Color, related_name='products', blank=True)

    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name='products', null=True)

    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Ensure that if is_discounted is True, discount_price is higher than 0
        if self.is_discounted and self.discount_percentage <= 0:
            raise ValueError("Discount percentage must be higher than 0 for discounted products.")
        super(Product, self).save(*args, **kwargs)

    @property
    def average_rating(self):
        avg_rating = self.ratings.aggregate(Avg('rating'))['rating__avg']
        return "{:.1f}".format(avg_rating) if avg_rating is not None else "0"

    @property
    def num_ratings(self):
        return self.ratings.count()

    @property
    def num_comments(self):
        return self.comments.count()

    @property
    def discounted_price(self):
        if self.is_discounted:
            # Calculate the discounted price based on the discount percentage
            discount_amount = (self.discount_percentage / 100) * self.price
            discounted_price = self.price - discount_amount
            return discounted_price
        else:
            return self.price

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='static/products/product_images/')

    def __str__(self):
        return f"Image{self.id} for {self.product.name}"


class ProductFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_features')
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        unique_together = ('title', 'product')

    def __str__(self):
        return f"{self.title} - {self.description} for {self.product.name}"
