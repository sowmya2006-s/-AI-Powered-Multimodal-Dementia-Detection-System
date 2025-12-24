from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase

class AuthAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'TestPass123!'
        }

    def test_signup(self):
        response = self.client.post('/api/accounts/signup/', self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_and_refresh(self):
        # Sign up first
        self.client.post('/api/accounts/signup/', self.user_data, format='json')
        # Login
        response = self.client.post('/api/accounts/login/', self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        refresh_token = response.data['refresh']
        # Refresh token
        refresh_response = self.client.post('/api/accounts/token/refresh/', {'refresh': refresh_token}, format='json')
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)
