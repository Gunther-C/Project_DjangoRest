from django.urls import path, include
from rest_framework import routers

from .views import RegisterApiView, LoginApiView, UserProfileViewSet

router = routers.SimpleRouter()
router.register('profile', UserProfileViewSet, basename='profile')

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('login/', LoginApiView.as_view(), name='login'),
    path('registration/', RegisterApiView.as_view(), name='register'),
    path('', include(router.urls)),
]

