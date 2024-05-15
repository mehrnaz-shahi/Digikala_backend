from rest_framework import serializers
from .models import Product, ProductImage, ProductFeature, Color
from comments.models import ProductComment
from score.models import ProductRating
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


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


class ProductCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        fields = ['user', 'product', 'text', 'created_at']


class ProductDetailSerializer(serializers.ModelSerializer):
    colors = ColorSerializer(many=True, read_only=True)  # Use ColorSerializer for colors field

    images = ProductImageSerializer(many=True, read_only=True)
    product_features = ProductFeatureSerializer(many=True, read_only=True)

    num_ratings = serializers.SerializerMethodField()
    num_comments = serializers.SerializerMethodField()

    avg_rating = serializers.SerializerMethodField()

    comments = ProductCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'categories', 'colors', 'retailer', 'avg_rating',
                  'num_ratings', 'images', 'comments',
                  'product_features', 'is_discounted', 'discount_percentage', 'discounted_price', 'num_comments']

    def get_discounted_price(self, obj):
        # Access the discounted_price property of the model instance
        return obj.discounted_price

    def get_num_ratings(self, obj):
        # Access the num_ratings property of the model instance
        return obj.num_ratings

    def get_num_comments(self, obj):
        # Access the num_comments property of the model instance
        return obj.num_comments

    def get_avg_rating(self, obj):
        # Access the num_comments property of the model instance
        return obj.average_rating


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


class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRating
        fields = ['id', 'product', 'rating', 'created_at']
        read_only_fields = ['created_at']




