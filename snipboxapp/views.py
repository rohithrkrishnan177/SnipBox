from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import Snippet, Tag
from .serializers import SnippetSerializer, TagSerializer, UserSerializer


class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(created_by=user)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        user = serializer.save()

        response_data = {
            "message": "User created successfully!",
            "user": {
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
