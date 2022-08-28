from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

class TestView(TestCase):

    def setUp(self):
      self.client = Client()
      self.create_user = reverse('create_user')
      self.newUser = User.objects.create_user(username='userTest2', password='password', email='test@email.com')

    def test_is_possible_to_sign_up_with_valid_informations(self):
        data = {
            'username': 'userTest',
            'email': 'userTest@email.com',
            'password': 'password'
        }
        response = self.client.post(self.create_user, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_unable_to_sign_up_with_invalid_email(self):
        data = {
            'email': 'userTest@email',
            'password': 'password',
            'username': 'userTest'
        }
        response = self.client.post(self.create_user, data)
        self.assertEqual(response.data['email'], ['Enter a valid email address.']) 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unable_to_sign_up_with_invalid_password(self):
        data = {
            'email': 'userTest@email.com',
            'password': 'passwor',
            'username': 'userTest'
        }
        response = self.client.post(self.create_user, data)
        self.assertEqual(response.data['password'], ['Ensure this field has at least 8 characters.']) 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unable_to_sign_up_with_invalid_username(self):
        data = {
            'email': 'userTest@email.com',
            'password': 'password',
            'username': 'us'
        }
        response = self.client.post(self.create_user, data)
        self.assertEqual(response.data['username'], ['Ensure this field has at least 3 characters.']) 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unable_to_sign_up_if_username_already_exists(self):
        data = {
            'email': 'userTest@email.com',
            'password': 'password',
            'username': 'userTest2'
        }
        response = self.client.post(self.create_user, data)
        self.assertEqual(response.data['username'], 'username already exists.') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)