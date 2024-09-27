# accounts/urls.py
from django.urls import path
from .views import CreateTokenView, OTPGenerateView, OTPVerifyView, SignUpView, LoginView, UserProfileView, verify_phone

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    # path('login/', LoginView.as_view(), name='login'),
    path('user/', UserProfileView.as_view(), name='profile-view'),
    path('login/', CreateTokenView.as_view(), name='auth-token'),
    path('send-otp/', OTPGenerateView.as_view(), name='send-otp'),
    path('verify-phone/', OTPVerifyView.as_view(), name='verify_phone'),
]
