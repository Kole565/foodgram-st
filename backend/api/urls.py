from django.urls import path, include
from rest_framework import routers

from .views import CustomUserViewSet


router = routers.DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
