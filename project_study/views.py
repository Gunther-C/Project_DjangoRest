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

    def get_queryset(self):
        return Project.objects.filter(project_shared__user=self.request.user)

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project, role='author')

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
            raise NotFound({'detail': 'Vous devez mettre un nom de contributeur'})

        username = " ".join(username.split())
        user = User.objects.get(username=username)
        if not user:
            raise NotFound({'detail': 'Ce nom n\'éxiste pas'})

        contributor = Contributor.objects.create(user=user, project=project, role='contributor')
        if contributor:
            return Response({'detail': 'Contributeur ajouté'}, status=status.HTTP_201_CREATED)
        return Response({'detail': 'le contributeur n\'est pas ajouté'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'],  permission_classes=[permissions.IsAuthenticated, IsAuthor])
    def del_contributor(self, request, pk):
        project = self.get_object()
        user = User.objects.get(username=request.data['username'])
        if user == project.author:
            raise ValidationError({"detail": "L'auteur ne peut pas être supprimé des contributeurs."})

        contributor = Contributor.objects.get(user=user, project=project)
        if contributor:
            contributor.delete()
            return Response({'detail': 'Contributeur supprimé'}, status=status.HTTP_201_CREATED)
        return Response({'detail': 'erreur'}, status=status.HTTP_400_BAD_REQUEST)



class ContributorViewSet(ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contributor.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        project_id = request.data.get('project')
        try:
            project = Project.objects.get(pk=project_id)

            if Contributor.objects.filter(user=self.request.user, project=project).exists():
                raise ValidationError({"detail": "Vous êtes déjà contributeur de ce projet."})

            Contributor.objects.create(user=self.request.user, project=project, role='contributor')

        except Project.DoesNotExist:
            raise NotFound({'detail': "Projet non trouvé."})

        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        project_name = request.data.get('project')
        project = Project.objects.get(name=project_name)
        if not project:
            raise ({"detail": "Projet non trouvé."})

        if self.request.user == project.author:
            raise ValidationError({"detail": "L'auteur ne peut pas se retirer du projet."})

        contributor = Contributor.objects.get(user=self.request.user, project=project)

        if contributor:
            contributor.delete()
            return Response({"detail": "Vous avez quitté le projet."}, status=status.HTTP_200_OK)
        return Response({"detail": "Vous n'êtes pas contributeur de ce projet."}, status=status.HTTP_400_BAD_REQUEST)




