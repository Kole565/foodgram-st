from django.contrib import admin
from django.urls import include, path
from recipes.views import RecipeViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
    path('s/<int:pk>', RecipeViewSet.as_view({"get": "retrieve"})),
]
