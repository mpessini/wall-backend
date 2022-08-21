from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view
from api.serializers import UserSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
def createUser(request):
    data = request.data
    serializer = UserSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        try:
            serializer.save()
            return Response(serializer.data)
        except:
            raise serializers.ValidationError({"status": "Username already exists"})