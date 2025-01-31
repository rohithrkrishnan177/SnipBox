from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, CreateUserView, CreateSnippetAPI, SnippetOverviewAPI, SnippetDetailAPI
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'tags', TagViewSet, basename='tag')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='login'),  # Login API
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create-user/', CreateUserView.as_view(), name='create_user'),
    path('create/', CreateSnippetAPI.as_view(), name='create_snippet'),
    path('snippets/', SnippetOverviewAPI.as_view(), name='snippet-overview'),
    path('snippets/<int:pk>/', SnippetDetailAPI.as_view(), name='snippet-detail'),
    path('snippets/create/', CreateSnippetAPI.as_view(), name='create-snippet'),

]
