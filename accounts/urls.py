from django.urls import path
from .views import SendOTPAPI, VerifyOTPAPI, UserInfoAPIView

urlpatterns = [
    path('sendOTP/', SendOTPAPI.as_view(), name='send_otp_code'),
    path('verifyOTP/', VerifyOTPAPI.as_view(), name='verify_otp_code'),
    path('whoami/', UserInfoAPIView.as_view(), name='whoami')

]