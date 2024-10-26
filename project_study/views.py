from django.contrib.auth import get_user_model
from rest_framework import status, permissions
from rest_framework.exceptions import PermissionDenied, ValidationError, NotFound
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .models import Project, Contributor
from .serializers import ProjectSerializer, ContributorSerializer
from .permissions import IsAuthorOrReadOnly, IsContributor, IsAuthor

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

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsContributor])
    def add_contributor(self, request, pk):
        project = self.get_object()
        contributor, created = Contributor.objects.get_or_create(
            user=self.request.user, project=project, role='contributor')

        if created:
            return Response({'detail': "Vous êtes maintenant contributeur du projet"},
                            status=status.HTTP_201_CREATED)
        return Response({'detail': "Vous êtes déja contributeur de ce projet."},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'],  permission_classes=[permissions.IsAuthenticated, IsContributor])
    def del_contributor(self, request, pk):
        project = self.get_object()

        try:
            contributor = Contributor.objects.get(user=self.request.user, project=project)
            contributor.delete()
            return Response({'detail': "Vous n'êtes plus contributeur du projet"}, status=status.HTTP_201_CREATED)

        except Contributor.DoesNotExist:
            raise ValidationError({"detail": "Vous n'êtes pas contributeur de ce projet."})


class ContributorViewSet(ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contributor.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        project_id = self.request.data.get('project')
        user_id = self.request.data.get('user')

        try:
            project = Project.objects.get(pk=project_id)
            user = User.objects.get(pk=user_id)

            if project.author != self.request.user:
                raise PermissionDenied({"detail": "Vous n'êtes pas l'auteur de ce projet"})

            if user == self.request.user:
                raise PermissionDenied({"detail": "Vous êtes déja l'auteur de ce projet"})

            serializer.save(user=user, project=project, role='contributor')

        except Project.DoesNotExist:
            raise ValidationError({"detail": "Le projet n'a pas été trouvé."})

        except User.DoesNotExist:
            raise ValidationError({"detail": "Cet utilisateur n'a pas été trouvé."})

    def perform_destroy(self, instance):
        project_id = self.request.data.get('project')
        user_id = self.request.data.get('user')

        try:
            project = Project.objects.get(pk=project_id)
            user = User.objects.get(pk=user_id)
            contributor = Contributor.objects.get(user=user, project=project)

            if contributor.project.author != self.request.user:
                raise PermissionDenied({"detail": "Vous n'êtes pas l'auteur de ce projet"})

            if contributor.user == self.request.user:
                raise PermissionDenied({"detail": "L'auteur ne peut pas se retirer du projet."})

            instance.delete()
            """
            instance.delete() ne correspond pas plutot contributor.delete()
            
            alors ou decorator @action
            ou récupérer id contributor avec instance.pk
            
            """

        except Project.DoesNotExist:
            raise ValidationError({"detail": "Le projet n'a pas été trouvé."})

        except User.DoesNotExist:
            raise ValidationError({"detail": "Cet utilisateur n'a pas été trouvé."})

        except Contributor.DoesNotExist:
            raise ValidationError({"detail": "Le contributeur n'a pas été trouvé."})








