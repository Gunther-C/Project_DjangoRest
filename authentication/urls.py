from rest_framework import routers
from django.urls import path, include

from .views import UserViewSet

router = routers.SimpleRouter()
router.register('auth', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
