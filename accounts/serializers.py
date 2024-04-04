from rest_framework import serializers
from .models import User, TemporaryUser
from django.core.validators import RegexValidator


class OTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        validators=[
              RegexValidator(
                     regex=r'^09\d{9}$',
                     message='Phone number must be 10 digits.',
                     code='invalid_phone_number'
                 )
             ]
         )
    otp_code = serializers.CharField(max_length=4)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number']


class UserInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class TempUserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r'^09\d{9}$',
                message='Phone number must be 10 digits.',
                code='invalid_phone_number'
            )
        ]
    )

    class Meta:
        model = TemporaryUser
        fields = ['phone_number']
