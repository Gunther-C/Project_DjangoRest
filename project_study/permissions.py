from rest_framework.permissions import BasePermission
from rest_framework.exceptions import ValidationError
from .models import Contributor, Project, Issue, Comment


class IsProjects(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_author = Contributor.objects.filter(user=request.user, project=obj, role='author').exists()
        if view.action in ['add_contributor', 'del_contributor']:
            return not is_author
        if view.action in ['update', 'partial_update', 'destroy']:
            return is_author
        return True


class IsContributors(BasePermission):
    def has_permission(self, request, view):
        project_id = request.query_params.get('project_id')
        if project_id:
            if not project_id.isdigit():
                raise ValidationError({"Detail": "Un nombre entier !"})
            return Contributor.objects.filter(project__id=project_id, user=request.user).exists()

        if view.action == 'create':
            project_id = request.data.get('project')
            if project_id:
                return Contributor.objects.filter(project__id=project_id, project__author=request.user).exists()
        return True

    def has_object_permission(self, request, view, obj):
        if view.action in ['destroy']:
            return obj.project.author == request.user
        if view.action in ['update', 'partial_update']:
            return False
        return obj.user == request.user


class IsIssue(BasePermission):
    def has_permission(self, request, view):
        project_id = request.query_params.get('project_id')
        if project_id:
            if not project_id.isdigit():
                raise ValidationError({"Detail": "Un nombre entier !"})
            return Issue.objects.filter(project__id=project_id,
                                        project__contributor_project__user=request.user).exists()
        return Issue.objects.filter(project__contributor_project__user=request.user).exists()

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update', 'destroy']:
            return obj.author.user == request.user
        return Issue.objects.filter(project__contributor_project__user=request.user).exists()


class IsComment(BasePermission):
    def has_permission(self, request, view):
        project_id = request.query_params.get('project_id')
        if project_id:
            if not project_id.isdigit():
                raise ValidationError({"Detail": "Un nombre entier !"})
            return Comment.objects.filter(issue__id=project_id,
                                          issue__project__contributor_project__user=request.user).exists()
        return Comment.objects.filter(issue__project__contributor_project__user=request.user).exists()

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update', 'destroy']:
            return obj.author.user == request.user
        return Comment.objects.filter(issue__project__contributor_project__user=request.user).exists()


