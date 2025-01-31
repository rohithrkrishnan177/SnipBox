from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SnippetViewSet, TagViewSet, CreateUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'snippets', SnippetViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='login'),  # Login API
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create-user/', CreateUserView.as_view(), name='create_user'),

]
