from rest_framework.permissions import BasePermission
from .models import Contributor, Project, Issue


class IsAuthorOrContributor(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_author = Contributor.objects.filter(user=request.user, project=obj, role='author').exists()
        if view.action in ['add_contributor', 'del_contributor']:
            return not is_author
        if view.action in ['update', 'partial_update', 'destroy']:
            return is_author
        return True


class IsAuthorProject(BasePermission):
    def has_permission(self, request, view):
        project_id = request.query_params.get('project_id')
        if project_id:
            return Contributor.objects.filter(project__id=project_id,
                                              project__author=request.user, role='contributor').exists()
        return Contributor.objects.filter(project__author=request.user, role='contributor').exists()

    def has_object_permission(self, request, view, obj):
        if view.action in ['create']:
            return obj.author == request.user
        return obj.project.author == request.user


class IsAuthorIssue(BasePermission):
    def has_object_permission(self, request, view, obj):

        if view.action in ['create']:
            return Contributor.objects.filter(user=request.user, project=obj.project).exists()
        return obj.author.user == request.user


class IsAuthorComment(BasePermission):
    def has_object_permission(self, request, view, obj):

        if view.action in ['create']:
            """Que issue exist et que user est contributeur"""
            return Contributor.objects.filter(project=obj.issue.project, user=self.request.user).exists()
        return obj.author.user == request.user




