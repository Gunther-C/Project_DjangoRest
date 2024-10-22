from django.urls import path, include
from rest_framework import routers

from .views import AddContributorAPIView, ProjectViewSet

router = routers.SimpleRouter()
router.register('project', ProjectViewSet, basename='project')


urlpatterns = [
    path('contributor_create/', AddContributorAPIView.as_view(), name='contributor-create'),
    path('', include(router.urls)),
]

# path('project_create/', CreateProjectAPIView.as_view(), name='project-create'),  CreateProjectAPIView,
