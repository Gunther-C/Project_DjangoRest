from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import status, permissions
from rest_framework.exceptions import PermissionDenied, ValidationError, NotFound
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from .permissions import IsProjects, IsContributors, IsIssue, IsComment

User = get_user_model()


class ProjectViewSet(ModelViewSet):
    """
    Filter : Un projet
    Filter : Tous les projets
    Filter : Tous les projets de l'utilisateur connecté
    Filter : Tous les projets dont l'utilisateur connecté est contributeur

    Option : L'utilisateur peut adhérer (contributeur) a un projet
    Option : L'utilisateur peut se retirer (contributeur) d'un projet
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjects]

    def get_queryset(self):
        query_author = self.request.query_params.get("author_only", "false").lower() == 'true'
        query_contributor = self.request.query_params.get("contributor_only", "false").lower() == 'true'

        if query_author:
            return self.queryset.filter(author=self.request.user)
        if query_contributor:
            return self.queryset.filter(contributor_project__user=self.request.user,
                                        contributor_project__role='contributor')
        return self.queryset

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project, role='author')

    @action(detail=True, methods=['post'])
    def add_contributor(self, request, pk):
        project = self.get_object()
        contributor, created = Contributor.objects.get_or_create(user=self.request.user, project=project,
                                                                 role='contributor')
        if created:
            return Response({'detail': "Vous êtes maintenant contributeur du projet"},
                            status=status.HTTP_201_CREATED)
        return Response({'detail': "Vous êtes déja contributeur de ce projet."},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def del_contributor(self, request, pk):
        project = self.get_object()
        try:
            contributor = Contributor.objects.get(user=self.request.user, project=project)
            contributor.delete()
            return Response({'detail': "Vous n'êtes plus contributeur du projet"}, status=status.HTTP_201_CREATED)

        except Contributor.DoesNotExist:
            raise NotFound({"Detail": "Aucun projet trouvé !"})


class ContributorViewSet(ModelViewSet):
    """
    Filter : Une contribution de l'utilisateur connecté
    Filter : Toutes les contributions de l'utilisateur connecté
    Filter : Tous les contributeurs d'un projet (l'utilisateur connecté est auteur ou contributeur)
    Filter : Tous les contributeurs des projets de l'utilisateur connecté
    """
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributors]

    def get_queryset(self):
        project_id = self.request.query_params.get('project_id')
        query_author = self.request.query_params.get("author_only", "false").lower() == 'true'

        if project_id:
            return self.queryset.filter(project__id=project_id)
        if query_author:
            return self.queryset.filter(project__author=self.request.user, role='contributor')
        return self.queryset.filter(user=self.request.user, role='contributor')

    def perform_create(self, serializer):
        project = serializer.validated_data.get('project')
        user = serializer.validated_data.get('user')

        # self.check_object_permissions(self.request, project)

        if Contributor.objects.filter(user=user, project=project, role='contributor').exists():
            raise ValidationError({"detail": "Cette utilisateur est déja contributeur de ce projet."})
        if user == self.request.user:
            raise PermissionDenied({"detail": "Vous êtes déja l'auteur de ce projet"})

        serializer.save(user=user, project=project, role='contributor')


class IssueViewSet(ModelViewSet):
    """
    Filter : Toutes les issues de l'utilisateur connecté
    Filter : Une issue d'un projet (l'utilisateur connecté est auteur ou contributeur)
    Filter : Toutes les issues d'un projet (l'utilisateur connecté est auteur ou contributeur)
    """
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsIssue]

    def get_queryset(self):
        project_id = self.request.query_params.get('project_id')
        if project_id:
            return self.queryset.filter(project__id=project_id)
        return self.queryset.filter(project__contributor_project__user=self.request.user)

    def perform_create(self, serializer):
        assigned_to = self.request.data.get('assigned_to')
        project = serializer.validated_data.get('project')
        author = get_object_or_404(Contributor, project=project, user=self.request.user)

        if assigned_to and not Contributor.objects.filter(project=project, pk=assigned_to).exists():
            raise ValidationError('L’utilisateur assigné doit être un contributeur du projet.')
        serializer.save(author=author)

    def perform_update(self, serializer):
        assigned_to = self.request.data.get('assigned_to')
        project = serializer.validated_data.get('project')

        if assigned_to and not Contributor.objects.filter(project=project, pk=assigned_to).exists():
            raise ValidationError('L’utilisateur assigné doit être un contributeur du projet.')
        serializer.save()


class CommentViewSet(ModelViewSet):
    """
    Filter : Tous les commentaires de l'utilisateur connecté
    Filter : Un commentaire (l'utilisateur connecté est auteur ou contributeur)
    Filter : Tous les commentaires d'une issue (l'utilisateur connecté est auteur ou contributeur)
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsComment]

    def get_queryset(self):
        issue_id = self.request.query_params.get('issue_id')
        if issue_id:
            return self.queryset.filter(issue__id=issue_id)
        return self.queryset.filter(author__user=self.request.user)

    def perform_create(self, serializer):
        issue = serializer.validated_data.get('issue')
        author = get_object_or_404(Contributor, project=issue.project, user=self.request.user)
        serializer.save(author=author)

    def perform_update(self, serializer):
        issue = serializer.validated_data.get('issue')
        if not Contributor.objects.filter(project=issue.project, user=self.request.user).exists():
            raise ValidationError("Cette issue ne fait pas partie d'un projet dont vous êtes contributeur.")
        serializer.save()

