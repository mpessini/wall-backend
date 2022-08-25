from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post_message = models.CharField(max_length=200, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.post_message[0:50]