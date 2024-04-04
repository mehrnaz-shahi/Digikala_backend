from rest_framework import serializers
from .models import Retailer


class RetailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retailer
        fields = ['name', 'location', 'contact_number', 'performance']
