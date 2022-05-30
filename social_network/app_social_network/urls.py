from django.urls import path, include
from rest_framework import routers
from .views import RegistrationAPIView, PostsViewSet, AddPostAPIView

router = routers.DefaultRouter()
router.register(r'posts', PostsViewSet)

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view(), name='registration'),
    path('posts/add/', AddPostAPIView.as_view(), name='add_post'),
    path('', include(router.urls)),
]
