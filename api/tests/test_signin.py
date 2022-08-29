from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

class TestView(TestCase):

    def setUp(self):
      self.client = Client()
      self.token_obtain_pair = reverse('token_obtain_pair')
      self.token_refresh = reverse('token_refresh')
      self.newUser = User.objects.create_user(username='userTest', password='password', email='test@email.com')

    def test_is_possible_to_sign_in_with_valid_credentials(self):
        userCredentials = {
            'username': 'userTest',
            'password': 'password'
        }
        response = self.client.post(self.token_obtain_pair, data=userCredentials)
        self.assertEqual(response.data.keys(), {'refresh', 'access'}) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_is_possible_to_update_tokens(self):
        userCredentials = {
            'username': 'userTest',
            'password': 'password'
        }
        tokens = self.client.post(self.token_obtain_pair, data=userCredentials)
        refresh = { 'refresh': tokens.data['refresh'] }
        response = self.client.post(self.token_refresh, data=refresh)
        self.assertEqual(response.data.keys(), {'refresh', 'access'}) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unable_to_sign_in_with_invalid_password(self):
        userCredentials = {
            'username': 'userTest',
            'password': 'invalidPassword'
        }
        response = self.client.post(self.token_obtain_pair, data=userCredentials)
        self.assertEqual(response.data['detail'], 'No active account found with the given credentials') 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_unable_to_sign_in_with_invalid_username(self):
        userCredentials = {
            'username': 'invalidUserTest',
            'password': 'password'
        }
        response = self.client.post(self.token_obtain_pair, data=userCredentials)
        self.assertEqual(response.data['detail'], 'No active account found with the given credentials') 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)