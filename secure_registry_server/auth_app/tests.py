from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class AuthAPITestCase(APITestCase):

    def setUp(self):
        # Optional: create a user for login tests
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='strongpassword123'
        )
        self.signup_url = reverse('signup')
        self.login_url = reverse('token_obtain_pair')
        self.refresh_url = reverse('token_refresh')

    # Signup Tests
    def test_signup_success(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword123"
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_signup_missing_fields(self):
        data = {"username": "", "password": ""}
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Login Tests
    def test_login_success(self):
        data = {"username": "testuser", "password": "strongpassword123"}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_wrong_credentials(self):
        data = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Refresh Token Tests
    def test_refresh_token_success(self):
        login_data = {"username": "testuser", "password": "strongpassword123"}
        login_response = self.client.post(self.login_url, login_data, format='json')
        refresh_token = login_response.data['refresh']

        response = self.client.post(self.refresh_url, {"refresh": refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_refresh_token_invalid(self):
        response = self.client.post(self.refresh_url, {"refresh": "invalidtoken"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
