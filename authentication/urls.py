
from django.urls import path, include
from .views import RegisterApiView, LoginApiView

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('', LoginApiView.as_view(), name='login'),
    path('registration/', RegisterApiView.as_view(), name='register'),
]
