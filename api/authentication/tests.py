from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import OTPCode


User = get_user_model()


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('token_obtain_pair')
        self.refresh_url = reverse('token_refresh')
        self.logout_url = reverse('logout')
        self.password_reset_request_url = reverse('password-reset-request')
        self.password_reset_verify_url = reverse('password-reset-verify')
        self.password_reset_url = reverse('password-reset')
        self.password_change_url = reverse('password-change')

        self.user_data = {
            'email': 'test@example.com',
            'password': 'TestPassword123!',
            'password2': 'TestPassword123!'
        }
        self.user = User.objects.create_user(
            email=self.user_data['email'],
            password=self.user_data['password']
        )

        response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        })
        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']

        self.authenticated_client = APIClient()
        self.authenticated_client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
    
    def test_user_registration(self):
        """Test user registration endpoint"""
        new_user_data = {
            'email': 'newuser@example.com',
            'password': 'NewPassword123!',
            'password2': 'NewPassword123!'
        }
        
        response = self.client.post(self.register_url, new_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)  # Original user + new user
        self.assertTrue('tokens' in response.data)
        self.assertTrue('access' in response.data['tokens'])
        self.assertTrue('refresh' in response.data['tokens'])
    
    def test_user_login(self):
        """Test user login endpoint"""
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)
    
    def test_token_refresh(self):
        """Test token refresh endpoint"""
        refresh_data = {
            'refresh': self.refresh_token
        }
        
        response = self.client.post(self.refresh_url, refresh_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
    
    def test_user_logout(self):
        """Test user logout endpoint"""
        logout_data = {
            'refresh': self.refresh_token
        }
        
        response = self.authenticated_client.post(self.logout_url, logout_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Successfully logged out')
    
    def test_password_reset_flow(self):
        """Test the complete password reset flow"""
        request_data = {
            'email': self.user_data['email']
        }
        
        response = self.client.post(self.password_reset_request_url, request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Password reset code has been sent to your email.')

        otp = OTPCode.objects.filter(email=self.user_data['email']).latest('created_at')

        verify_data = {
            'email': self.user_data['email'],
            'code': otp.code
        }
        
        response = self.client.post(self.password_reset_verify_url, verify_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Code verified successfully. You can now reset your password.')

        reset_data = {
            'email': self.user_data['email'],
            'code': otp.code,
            'password': 'NewPassword123!',
            'password2': 'NewPassword123!'
        }
        
        response = self.client.post(self.password_reset_url, reset_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Password has been reset successfully.')

        login_data = {
            'email': self.user_data['email'],
            'password': 'NewPassword123!'
        }
        
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_password_change(self):
        """Test password change endpoint"""
        change_data = {
            'old_password': self.user_data['password'],
            'new_password': 'ChangedPassword123!',
            'new_password2': 'ChangedPassword123!'
        }
        
        response = self.authenticated_client.put(self.password_change_url, change_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Password changed successfully.')

        login_data = {
            'email': self.user_data['email'],
            'password': 'ChangedPassword123!'
        }
        
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_invalid_registration(self):
        """Test registration with invalid data"""
        invalid_data = {
            'email': 'invalid@example.com',
            'password': 'Password123!',
            'password2': 'DifferentPassword123!'
        }
        
        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('password' in response.data)

        existing_data = {
            'email': self.user_data['email'],
            'password': 'Password123!',
            'password2': 'Password123!'
        }
        
        response = self.client.post(self.register_url, existing_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_invalid_login(self):
        """Test login with invalid credentials"""
        invalid_data = {
            'email': self.user_data['email'],
            'password': 'WrongPassword123!'
        }
        
        response = self.client.post(self.login_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        non_existent_data = {
            'email': 'nonexistent@example.com',
            'password': 'Password123!'
        }
        
        response = self.client.post(self.login_url, non_existent_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_invalid_password_reset(self):
        """Test password reset with invalid data"""
        request_data = {
            'email': 'nonexistent@example.com'
        }
        
        response = self.client.post(self.password_reset_request_url, request_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        verify_data = {
            'email': self.user_data['email'],
            'code': '000000'
        }
        
        response = self.client.post(self.password_reset_verify_url, verify_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        otp = OTPCode.objects.create(
            email=self.user_data['email'],
            code='123456'
        )
        otp.is_verified = True
        otp.save()
        
        reset_data = {
            'email': self.user_data['email'],
            'code': otp.code,
            'password': 'NewPassword123!',
            'password2': 'DifferentPassword123!'
        }
        
        response = self.client.post(self.password_reset_url, reset_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_invalid_password_change(self):
        """Test password change with invalid data"""
        invalid_data = {
            'old_password': 'WrongPassword123!',
            'new_password': 'NewPassword123!',
            'new_password2': 'NewPassword123!'
        }
        
        response = self.authenticated_client.put(self.password_change_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        mismatched_data = {
            'old_password': self.user_data['password'],
            'new_password': 'NewPassword123!',
            'new_password2': 'DifferentPassword123!'
        }
        
        response = self.authenticated_client.put(self.password_change_url, mismatched_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_unauthorized_access(self):
        """Test unauthorized access to protected endpoints"""
        logout_data = {
            'refresh': self.refresh_token
        }
        
        response = self.client.post(self.logout_url, logout_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        change_data = {
            'old_password': self.user_data['password'],
            'new_password': 'NewPassword123!',
            'new_password2': 'NewPassword123!'
        }
        
        response = self.client.put(self.password_change_url, change_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
