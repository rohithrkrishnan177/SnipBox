from django.contrib.auth.models import User
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import Tag, Snippet
from .serializers import SnippetSerializer, TagSerializer, UserSerializer


# Create TAG API
class CreateTagAPI(generics.CreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]


# Create API
class CreateSnippetAPI(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can create snippets
    serializer_class = SnippetSerializer

    def perform_create(self, serializer):
        # Set the user to the current authenticated user
        serializer.save(created_by=self.request.user)


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


class SnippetOverviewAPI(generics.ListAPIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this API
    serializer_class = SnippetSerializer

    def get_queryset(self):
        # Filter snippets by the authenticated user
        return Snippet.objects.filter(created_by=self.request.user)

    def list(self, request, *args, **kwargs):
        # Get the list of snippets for the current user
        snippets = self.get_queryset()

        # Count the total number of snippets
        total_count = snippets.count()

        # Serialize the snippets
        serializer = self.get_serializer(snippets, many=True)

        # Build the response with total count and snippets
        return Response({
            "total_count": total_count,
            "snippets": serializer.data
        })


class SnippetDetailAPI(generics.RetrieveAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
