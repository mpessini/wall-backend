from django.template.loader import render_to_string 
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, PostSerializer
from .models import Post

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'token',
        'token/refresh',
        'signup/',
        'posts/',
        'post/new/'
    ]
    return Response(routes)

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
    context = {'username': data['username']}
    message = render_to_string('registration-account.txt.j2', context)
    html_message = render_to_string('registration-account.html.j2', context)
    serializer = UserSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        try:
            serializer.save()
            send_mail(
                '[Wall App]Account Registration',
                message,
                settings.EMAIL_HOST_USER,
                [data['email']],
                fail_silently=False,
                html_message=html_message
            )
            return Response(serializer.data, status=201)
        except:
            raise serializers.ValidationError({'username': 'username already exists.'})

@api_view(['GET'])
def getPosts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createPost(request):
    data = request.data
    if (len(data['post_message']) == 0):
        raise serializers.ValidationError({'Post': "Post can't be empty."})
    post_message = Post.objects.create(
        owner = request.user,
        post_message=data['post_message']
    )
    serializer = PostSerializer(post_message, many=False)
    return Response(serializer.data)
