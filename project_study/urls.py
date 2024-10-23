from django.urls import path, include
from rest_framework import routers

from .views import ProjectViewSet, ContributorViewSet

router = routers.SimpleRouter()
router.register('project', ProjectViewSet, basename='project')
router.register('contributor', ContributorViewSet, basename='contributor')


urlpatterns = [
    path('', include(router.urls)),
]

