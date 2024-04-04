from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.utils import timezone
from .serializers import OTPSerializer, UserSerializer, TempUserSerializer, UserInformationSerializer
from .models import TemporaryUser
from .utils import generate_otp
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication


User = get_user_model()


def expiration_timestamp():
    expiration_duration = timezone.timedelta(minutes=3)
    return timezone.now() + expiration_duration


class SendOTPAPI(CreateAPIView):
    queryset = TemporaryUser.objects.all()
    serializer_class = TempUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data.get('phone_number')
            # Try to get existing user
            user, created = TemporaryUser.objects.update_or_create(
                phone_number=phone_number,
                defaults={
                    'otp_code': generate_otp(),
                    'otp_code_expiration': expiration_timestamp()
                }
            )

            print(f"OTP Code for {phone_number}: {user.otp_code}")
            return Response({"detail": "OTP sent successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPAPI(CreateAPIView):
    def create(self, request, *args, **kwargs):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            otp_code = serializer.validated_data['otp_code']
            phone_number = request.data.get('phone_number')
            user = TemporaryUser.objects.filter(phone_number=phone_number, otp_code=otp_code).first()
            if user:
                if user.is_otp_valid():
                    # OTP code is valid
                    # Check if user already exists or create new user
                    auth_user = self.authenticate_or_create_user(user)
                    if auth_user:
                        # Generate tokens
                        tokens = self.get_tokens(auth_user)
                        login(request, auth_user)
                        user.delete()  # delete temp user after login successfully
                        return Response(tokens, status=status.HTTP_200_OK)
                return Response({"detail": "Invalid or expired OTP code"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"detail": "You should give otp code first"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def authenticate_or_create_user(self, temp_user):
        # Check if user with phone number exists
        user = User.objects.filter(phone_number=temp_user.phone_number).first()
        if user:
            return user
        # Create new user based on temporary user info
        new_user = User.objects.create_user(
            phone_number=temp_user.phone_number,
            password=temp_user.otp_code
        )
        return new_user

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }

    # Optional: Override the get_serializer_class method to specify serializer class
    def get_serializer_class(self):
        return OTPSerializer  # Specify your serializer class here


class UserInfoAPIView(RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserInformationSerializer

    def get_object(self):
        # The authenticated user can be accessed via self.request.user
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)