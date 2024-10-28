from django.contrib.auth import get_user_model
from rest_framework import status, permissions
from rest_framework.exceptions import PermissionDenied, ValidationError, NotFound
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly, IsContributor, IsAuthor

User = get_user_model()


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(contributor_project__user=self.request.user)

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
        return Contributor.objects.filter(project__author=self.request.user, role='contributor')

    def perform_create(self, serializer):
        project_id = self.request.data.get('project')
        user_id = self.request.data.get('user')

        project = Project.objects.get(pk=project_id)
        user = User.objects.get(pk=user_id)
        contributor = Contributor.objects.filter(user=user, project=project, role='contributor').exists()

        if contributor:
            raise ValidationError({"detail": "Cette utilisateur est déja contributeur de ce projet."})

        if project.author != self.request.user:
            raise PermissionDenied({"detail": "Vous n'êtes pas l'auteur de ce projet"})

        if user == self.request.user:
            raise PermissionDenied({"detail": "Vous êtes déja l'auteur de ce projet"})

        serializer.save(user=user, project=project, role='contributor')


class IssueViewSet(ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Issue.objects.filter(project__contributor_project__user=self.request.user)

    def perform_create(self, serializer):
        assigned_to = serializer.validated_data.get('assigned_to')
        project = serializer.validated_data.get('project')

        if assigned_to and not Contributor.objects.filter(project=project, user=assigned_to).exists():
            raise ValidationError('L’utilisateur assigné doit être un contributeur du projet.')

        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(issue__project__contributor_project__user=self.request.user)

    def perform_create(self, serializer):
        issue = serializer.validated_data.get('issue')
        if not Contributor.objects.filter(project=issue.project, user=self.request.user).exists():
            raise ValidationError('Vous devez être contributeur du projet pour créer un commentaire.')
        serializer.save(author=self.request.user)
