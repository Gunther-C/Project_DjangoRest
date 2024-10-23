from django.contrib.auth import get_user_model

from rest_framework import status, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .models import Project, Contributor
from .serializers import ProjectSerializer, AddContributorSerializer
from .permissions import IsAuthorOrReadOnly

User = get_user_model()


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Project.objects.filter(project_shared__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        project = self.get_object()
        if self.request.user != project.author:
            raise PermissionDenied({"detail": "Vous n'êtes pas autorisé à modifier ce projet."})
        serializer.save()

    def perform_destroy(self, instance):
        project = self.get_object()
        if self.request.user != project.author:
            raise PermissionDenied({"detail": "Vous n'êtes pas autorisé à supprimer ce projet."})
        instance.delete()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsAuthorOrReadOnly])
    def add_contributor(self, request, pk):
        project = self.get_object()
        serializer = AddContributorSerializer(data=request.data, context={'project': project})
        if serializer.is_valid():
            serializer.save()

    @action(detail=True, methods=['delete'],  permission_classes=[permissions.IsAuthenticated, IsAuthorOrReadOnly])
    def del_contributor(self, request, pk):
        project = self.get_object()
        user = User.objects.get(username=request.data['username'])
        contributor = Contributor.objects.get(user=user, project=project)
        contributor.delete()
