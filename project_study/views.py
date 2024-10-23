from django.contrib.auth import get_user_model

from rest_framework import status, permissions
from rest_framework.exceptions import PermissionDenied, ValidationError, NotFound
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .models import Project, Contributor
from .serializers import ProjectSerializer, ContributorSerializer
from .permissions import IsAuthorOrReadOnly, IsAuthor

User = get_user_model()


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    """ PERMISSION A VOIR LES VUES POUR CONTRIBUTORS UNIQUE MAIS LA CREATION JUSTE AUTHENTICATED"""
    def get_queryset(self):
        return Project.objects.filter(project_shared__user=self.request.user)

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        Contributor.object.create(user=self.request.user, project=project, role='author')

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

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsAuthor])
    def add_contributor(self, request, pk):
        project = self.get_object()
        username = request.data.get('username')
        if not username:
            raise NotFound({'detail': 'Vous devez mettre un nom d\'utilisateur'})

        username = " ".join(username.split())
        user = User.objects.get(username=username)
        if not user:
            raise NotFound({'detail': 'Ce nom n\'éxiste pas'})

        serializer = AddContributorSerializer(data=request.data, context={'project': project, 'role': 'contributor'})
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'],  permission_classes=[permissions.IsAuthenticated, IsAuthor])
    def del_contributor(self, request, pk):
        project = self.get_object()
        user = User.objects.get(username=request.data['username'])
        if user == project.author:
            raise ValidationError({"detail": "L'auteur ne peut pas être supprimé des contributeurs."})

        contributor = Contributor.objects.get(user=user, project=project)
        contributor.delete()


class ContributorViewSet(ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributor]

    def get_queryset(self):
        return Project.objects.filter(project_contributor__user=self.request.user)







