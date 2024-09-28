# accounts/views.py
from datetime import timedelta
from django.utils import timezone
from rest_framework import status, authentication, permissions
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny

from accounts import models
from accounts.utils import SMSService, generate_otp
from .serializers import AuthTokenSerializer, OTPSerializer, OTPcreateSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.settings import api_settings

User = get_user_model()


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(email=response.data['email'])
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': response.data})


class CreateTokenView(ObtainAuthToken):
    """Create new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Retrive and Update authenticated user profile"""
    # queryset = models.User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrive and return authenticated user"""
        return models.CustomUser.objects.get(pk=self.request.user.pk)


class OTPGenerateView(generics.CreateAPIView):
    serializer_class = OTPcreateSerializer
    def post(self, request, *args, **kwargs):

        user = request.data.get('email')
        user_inst = models.CustomUser.objects.get(email=user)
        if user and user_inst.phone_number:
            otp_obj = models.Otp.objects.get_or_create(email=user)[0]  # Adjust expiration time as needed 
            otp = generate_otp()  # Replace with your OTP generation logic
            
            otp_obj.pin = otp
            otp_obj.expired_at = timezone.now() + timedelta(minutes=5)
            otp_obj.save()

            SMSService().send_otp(user_inst.phone_number, otp)  # Replace with your OTP sending logic
            return Response({'detail': 'OTP sent successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'Error'}, status=status.HTTP_400_BAD_REQUEST)


class OTPVerifyView(generics.GenericAPIView):
    serializer_class = OTPSerializer
    # permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        otp = request.data.get('pin')
        try:
            otp_obj = models.Otp.objects.get(email=email, pin=otp, expired_at__gte=timezone.now())
            user = models.User.objects.get(email=email)
            user.is_active = True
            otp_obj.delete()
            user.save()
            return Response({'status': 'success', 'message': 'Phone number verified, account activated!'}, status=status.HTTP_200_OK)

        except models.Otp.DoesNotExist:
            return Response({'status': 'success', 'message': 'Invalid OTP code'}, status=status.HTTP_400_BAD_REQUEST)