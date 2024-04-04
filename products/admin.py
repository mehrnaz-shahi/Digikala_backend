from django.contrib import admin
from .models import Product, ProductImage, ProductFeature, Category, Color

# admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductFeature)
admin.site.register(Category)
admin.site.register(Color)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_discounted', 'discount_percentage']
    list_filter = ['is_discounted']

