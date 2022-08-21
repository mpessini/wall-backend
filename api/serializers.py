from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField(min_length=3, max_length=24)
    password = serializers.CharField(min_length=8, max_length=50)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
          'password': {'write_only': True, "required": True}
        }

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            return user