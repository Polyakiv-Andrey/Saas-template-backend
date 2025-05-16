from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .tasks import send_password_reset_email
import random
import string
from .models import OTPCode

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'tokens')
        extra_kwargs = {
            'tokens': {'read_only': True}
        }

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.USERNAME_FIELD


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            self.user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def save(self):
        user = self.user
        reset_code = ''.join(random.choices(string.digits, k=6))
        OTPCode.objects.create(
            email=user.email,
            code=reset_code
        )
        send_password_reset_email.delay(user.email, reset_code)


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(min_length=6, max_length=6)

    def validate(self, attrs):
        try:
            otp = OTPCode.objects.filter(
                email=attrs['email'],
                code=attrs['code'],
                is_verified=False
            ).latest('created_at')
            
            if not otp.is_valid():
                raise serializers.ValidationError({"code": "Code has expired."})
            
            self.otp = otp
            return attrs
        except OTPCode.DoesNotExist:
            raise serializers.ValidationError({"code": "Invalid code."})


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(min_length=6, max_length=6)
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        try:
            otp = OTPCode.objects.filter(
                email=attrs['email'],
                code=attrs['code'],
                is_verified=True
            ).latest('created_at')
            
            if not otp.is_valid():
                raise serializers.ValidationError({"code": "Code has expired or is invalid."})
            
            self.otp = otp
            return attrs
        except OTPCode.DoesNotExist:
            raise serializers.ValidationError({"code": "Invalid or unverified code."})


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_active', 'is_staff', 'is_superuser']