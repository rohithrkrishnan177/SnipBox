from django.contrib.auth.models import User
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from .models import Tag, Snippet
from .serializers import SnippetSerializer, TagSerializer, UserSerializer, SnippetOverViewSerializer, \
    SnippetViewSetSerializer, TagListSerializer


# Create Snippet API
class CreateSnippetAPI(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SnippetSerializer

    def get_serializer_context(self):
        return {'request': self.request}  # Pass the request context

    def perform_create(self, serializer):
        serializer.save()


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]  # Requires authentication to access


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
    serializer_class = SnippetOverViewSerializer

    def get_queryset(self):
        return Snippet.objects.all()

    def list(self, request, *args, **kwargs):
        # Get the list of snippets for the current user
        snippets = self.get_queryset()

        # Count the total number of snippets
        total_count = snippets.count()

        # Serialize the snippets
        serializer = self.get_serializer(snippets, many=True, context={'request': request})

        # Build the response with total count and snippets
        return Response({
            "total_count": total_count,
            "snippets": serializer.data
        })


class SnippetDetailAPI(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SnippetViewSetSerializer

    def get_queryset(self):
        # Return all snippets related to the logged-in user
        return Snippet.objects.filter(created_by=self.request.user)

    def perform_update(self, serializer):
        # Perform the update operation (already handled by ModelViewSet)
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """
        Delete the selected snippet and return the list of remaining snippets.
        """
        instance = self.get_object()
        self.perform_destroy(instance)

        # Return the list of remaining snippets
        snippets = Snippet.objects.filter(created_by=request.user)
        serializer = SnippetViewSetSerializer(snippets, many=True)  # Using the custom serializer
        return Response(serializer.data)


class TagDetailAPI(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TagListSerializer

    def get_queryset(self):
        """
        This query ensures that only tags that belong to the logged-in user are fetched.
        """
        return Tag.objects.all()

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a tag and the snippets linked to it.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
