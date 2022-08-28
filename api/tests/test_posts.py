from django.test import TestCase, Client
from django.contrib.auth.models import User
from api.models import Post
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

class TestView(TestCase):

    def setUp(self):
      self.client = Client()
      self.token_obtain_pair = reverse('token_obtain_pair')
      self.token_refresh = reverse('token_refresh')
      self.post_list = reverse('post_list')
      self.create_post = reverse('create_post')
      self.newUser = User.objects.create_user(username='userTest', password='password', email='test@email.com')
      self.newPost = Post.objects.create(owner=self.newUser, post_message='My Test Post Message')
      self.token = RefreshToken.for_user(self.newUser)

    def test_posts_are_listed_correctly(self):
        response = self.client.get(self.post_list)
        post = response.data[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post['id'], 1) 
        self.assertEqual(post['post_message'], 'My Test Post Message') 
        self.assertEqual(post['owner']['username'], 'userTest') 
        self.assertEqual(post.keys(), {'id', 'owner', 'post_message', 'created_at', 'update_at'})
        self.assertEqual(post['owner'].keys(), {'id', 'username'})

    def test_unable_to_create_a_post_if_unauthenticated(self):
        post = {'post_message': 'Trying to create a post unauthenticated.'}
        response = self.client.post(self.create_post, data=post)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_is_possible_to_create_a_post_if_authenticated(self):
        post = {'post_message': 'Trying to create a post authenticated.'}
        response = self.client.post(self.create_post, data=post, **{ 'HTTP_AUTHORIZATION': f'Bearer {self.token.access_token}' })
        post = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post['id'], 2) 
        self.assertEqual(post['post_message'], 'Trying to create a post authenticated.') 
        self.assertEqual(post['owner']['username'], 'userTest') 
        self.assertEqual(post.keys(), {'id', 'owner', 'post_message', 'created_at', 'update_at'})
        self.assertEqual(post['owner'].keys(), {'id', 'username'})
    
    def test_posts_are_listed_after_create_a_new_one(self):
        post = {'post_message': 'My second post message.'}
        self.client.post(self.create_post, data=post, **{ 'HTTP_AUTHORIZATION': f'Bearer {self.token.access_token}' })
        response = self.client.get(self.post_list)
        post = response.data[1]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(post['post_message'], 'My second post message.') 