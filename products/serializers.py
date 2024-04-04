from rest_framework import serializers
from .models import Product, ProductImage, ProductFeature, Color


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeature
        fields = ['title', 'description']


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'code']


class ProductDetailSerializer(serializers.ModelSerializer):
    colors = ColorSerializer(many=True, read_only=True)  # Use ColorSerializer for colors field

    images = ProductImageSerializer(many=True, read_only=True)
    product_features = ProductFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'categories', 'colors', 'retailer', 'average_rating', 'images',
                  'product_features', 'is_discounted', 'discount_percentage', 'discounted_price']

    def get_discounted_price(self, obj):
        # Access the discounted_price property of the model instance
        return obj.discounted_price


class ProductSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=True)
    first_image = serializers.SerializerMethodField()

    amazing = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'first_image', 'images', 'price', 'average_rating', 'amazing',
                  'is_discounted', 'discount_percentage', 'discounted_price']

    def get_discounted_price(self, obj):
        # Access the discounted_price property of the model instance
        return obj.discounted_price

    def get_amazing(self, obj):
        # Calculate the amazing field based on the discount percentage
        return obj.discount_percentage >= 20

    def get_first_image(self, obj):
        first_image_url = None
        if obj.images.exists():
            first_image_url = self.context['request'].build_absolute_uri(obj.images.first().image.url)
        return first_image_url

    def to_representation(self, instance):
        # Call the parent to_representation method
        ret = super().to_representation(instance)
        # Remove 'images' key if present (already handled by 'first_image')
        ret.pop('images', None)
        return ret
