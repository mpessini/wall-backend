from django.test import TestCase
from django.urls import reverse, resolve
from api.views import getPosts, createPost, createUser, MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

class TestView(TestCase):

    def test_user_sign_in_url(self):
        path = reverse('token_obtain_pair')
        resolvedPath = resolve(path).func.view_class
        self.assertEqual(resolvedPath, MyTokenObtainPairView)
    
    def test_user_update_tokens(self):
        path = reverse('token_refresh')
        resolvedPath = resolve(path).func.view_class
        self.assertEqual(resolvedPath, TokenRefreshView)
    
    def test_create_new_user_url(self):
        path = reverse('create_user')
        resolvedPath = resolve(path).func
        self.assertEqual(resolvedPath, createUser)
    
    def test_get_posts_list_url(self):
        path = reverse('post_list')
        resolvedPath = resolve(path).func
        self.assertEqual(resolvedPath, getPosts)

    def test_create_new_post_url(self):
        path = reverse('create_post')
        resolvedPath = resolve(path).func
        self.assertEqual(resolvedPath, createPost)
