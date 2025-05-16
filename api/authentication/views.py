from urllib.parse import urlencode

from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponseRedirect

from saas_template_backend import settings
from .serializers import (
    RegisterSerializer,
    CustomTokenObtainPairSerializer,
    PasswordResetRequestSerializer,
    PasswordResetSerializer,
    ChangePasswordSerializer,
    VerifyOTPSerializer, UserSerializer,
)

from social_django.utils import load_strategy, load_backend
from social_core.exceptions import AuthForbidden
import logging


User = get_user_model()
logger = logging.getLogger(__name__)


class RegisterView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PasswordResetRequestView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    @swagger_auto_schema(
        operation_description="Step 1: Request password reset code",
        request_body=PasswordResetRequestSerializer,
        responses={
            200: openapi.Response(
                description="Password reset code sent successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Password reset code has been sent to your email."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    @swagger_auto_schema(
        operation_description="Step 2: Verify OTP code",
        request_body=VerifyOTPSerializer,
        responses={
            200: openapi.Response(
                description="OTP code verified successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.otp
            otp.is_verified = True
            otp.save()
            return Response(
                {"message": "Code verified successfully. You can now reset your password."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    @swagger_auto_schema(
        operation_description="Step 3: Reset password using verified code",
        request_body=PasswordResetSerializer,
        responses={
            200: openapi.Response(
                description="Password reset successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.validated_data['email'])
            user.set_password(serializer.validated_data['password'])
            user.save()

            otp = serializer.otp
            otp.is_verified = False
            otp.save()
            
            return Response(
                {"message": "Password has been reset successfully."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(
                {"message": "Password changed successfully."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(
        operation_description="Logout user and blacklist refresh token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token to blacklist'),
            },
            required=['refresh']
        ),
        responses={
            200: openapi.Response(
                description="Successfully logged out",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            400: "Bad Request"
        }
    )
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response(
                {"message": "Successfully logged out"}, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": "Invalid token or token has expired"}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class GoogleLoginView(APIView):
    def get(self, request):
        strategy = load_strategy(request)
        strategy.session_set("redirect_uri", settings.SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI)
        backend_name = 'google-oauth2'
        backend = load_backend(
            strategy,
            backend_name,
            redirect_uri=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI
        )
        auth_url = backend.auth_url() + '&prompt=select_account'
        return HttpResponseRedirect(auth_url)


class GoogleCallbackView(APIView):
    def get(self, request):
        try:
            strategy = load_strategy(request)
            strategy.session_set("redirect_uri", settings.SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI)
            backend_name = 'google-oauth2'
            backend = load_backend(
                strategy,
                backend_name,
                redirect_uri=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI
            )
            
            user = backend.complete(request=request)
            
            if not user:
                return Response(
                    {'error': 'Authentication failed'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                user_obj = User.objects.get(email=user.email)
            except User.DoesNotExist:
                user_obj = User.objects.create_user(
                    email=user.email,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    is_active=True
                )
                user_obj.set_unusable_password()
                user_obj.save()

            refresh = RefreshToken.for_user(user_obj)
            params = urlencode({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'email': user_obj.email,
            })
            frontend = settings.FRONTEND_URL
            return HttpResponseRedirect(f'{frontend}auth/google/callback?{params}')

        except AuthForbidden as e:
            logger.error(f"Google OAuth error: {str(e)}")
            return Response(
                {'error': 'Authentication failed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Unexpected error during Google OAuth: {str(e)}")
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)