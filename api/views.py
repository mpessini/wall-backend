from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, PostSerializer
from .models import Post

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
            raise serializers.ValidationError({"Username": "Username already exists"})

@api_view(['GET'])
def getPosts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createPost(request):
    data = request.data
    if (len(data['post']) == 0):
        raise serializers.ValidationError({"Post": "Post can't be empty."})
    post_message = Post.objects.create(
        owner = request.user,
        post=data['post']
    )
    serializer = PostSerializer(post_message, many=False)
    return Response(serializer.data)