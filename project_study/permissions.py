from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied, ValidationError, NotFound
from .models import Contributor, Project, Issue


class IsAuthorOrContributor(BasePermission):
    def has_permission(self, request, view):
        query_params = request.query_params
        for params in query_params:
            if params != 'author_only' and params != 'contributor_only':
                # raise ValidationError({"Detail": "Ce paramètre n'éxiste pas !"})
                return False
            if query_params.get(params) != 'true' and query_params.get(params) != 'false':
                # raise ValidationError({"Detail": "La valeur du paramètre additionnel doit être `true` ou `false` !"})
                return False
        return True

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
        query_author = request.query_params.get('author_only')

        if project_id:
            _id = project_id.isdigit()
            if not _id:
                return False
            return Contributor.objects.filter(project__id=project_id, user=request.user).exists()

        elif query_author:
            return Contributor.objects.filter(project__author=request.user, role='contributor').exists()

    def has_object_permission(self, request, view, obj):
        if view.action in ['create']:
            return obj.author == request.user
        return obj.project.author == request.user


class IsAuthorIssue(BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action in ['create'] or request.method in permissions.SAFE_METHODS:
            return Contributor.objects.filter(project=obj.project, user=request.user).exists()
        return obj.author.user == request.user


class IsAuthorComment(BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action in ['create'] or request.method in permissions.SAFE_METHODS:
            return Contributor.objects.filter(project=obj.issue.project, user=request.user).exists()
        return obj.author.user == request.user
