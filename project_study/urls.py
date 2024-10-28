from django.urls import path, include
from rest_framework import routers

from .views import ProjectViewSet, ContributorViewSet, IssueViewSet, CommentViewSet

router = routers.SimpleRouter()
router.register('project', ProjectViewSet, basename='project')
router.register('contributor', ContributorViewSet, basename='contributor')
router.register('issue', IssueViewSet, basename='issue')
router.register('comment', CommentViewSet, basename='comment')


urlpatterns = [
    path('', include(router.urls)),
]
