# accounts/serializers.py
from django.utils.translation import gettext as _
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .utils import SMSService, generate_otp
from .models import Otp

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'full_name', 'password', 'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data.get('full_name', ''),
            phone_number=validated_data.get('phone_number', None),
        )
        
        # Generate and send OTP if phone number exists
        if user.phone_number:
            otp = generate_otp()  # 6-digit OTP
            sms_service = SMSService()
            sms_service.send_otp(user.phone_number, otp)

            # Save OTP to user profile (store in a temporary field or another model)
            otp_obj = Otp.objects.get_or_create(email=user.email, pin=otp)[0]
            otp_obj.expired_at = timezone.now() + timedelta(minutes=5)
            otp_obj.save()
        
        return user

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = ('email', 'pin', 'created_at', 'expired_at')
        read_only_fields = ('created_at', 'expired_at')


class OTPcreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = ('email', 'created_at', 'expired_at')
        read_only_fields = ('created_at', 'expired_at')


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=True,
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user_obj = get_user_model().objects.get(email=email)
            if user_obj.check_password(password):
                user = user_obj
            else:
                user = None
        except get_user_model().DoesNotExist:
            user = None
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs
