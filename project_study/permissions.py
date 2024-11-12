from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied, ValidationError, NotFound
from .models import Contributor, Project, Issue, Comment


class IsProjects(BasePermission):
    def has_permission(self, request, view):
        query_params = request.query_params
        for params in query_params:
            if params not in ['author_only', 'contributor_only']:
                # raise ValidationError({"Detail": "Ce paramètre n'éxiste pas !"})
                return False
            if query_params.get(params) not in ['true', 'false']:
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


class IsContributors(BasePermission):
    def has_permission(self, request, view):
        query_params = request.query_params
        for params in query_params:
            if params not in ['project_id', 'author_only']:
                return False

            if params == 'project_id':
                project_id = query_params.get(params)
                if not project_id.isdigit():
                    return False
                return Contributor.objects.filter(project__id=project_id, user=request.user).exists()

            if params == 'author_only':
                if query_params.get(params) not in ['true', 'false']:
                    return False
                return Contributor.objects.filter(project__author=request.user, role='contributor').exists()
        return True

    def has_object_permission(self, request, view, obj):
        if view.action in ['create']:
            return obj.author == request.user
        if view.action in ['destroy']:
            return obj.project.author == request.user
        if view.action in ['update', 'partial_update']:
            return False
        return obj.user == request.user


class IsIssue(BasePermission):
    def has_permission(self, request, view):
        query_params = request.query_params
        for params in query_params:
            if params not in ['project_id']:
                return False

            project_id = query_params.get(params)
            if not project_id.isdigit():
                return False
            return Issue.objects.filter(project__id=project_id,
                                        project__contributor_project__user=request.user).exists()
        return Issue.objects.filter(project__contributor_project__user=request.user).exists()

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update', 'destroy']:
            return obj.author.user == request.user
        return Issue.objects.filter(project__contributor_project__user=request.user).exists()


class IsComment(BasePermission):
    def has_permission(self, request, view):
        query_params = request.query_params
        for params in query_params:
            if params not in ['issue_id']:
                return False

            project_id = query_params.get(params)
            if not project_id.isdigit():
                return False
            return Comment.objects.filter(issue__id=project_id,
                                          issue__project__contributor_project__user=request.user).exists()
        return Comment.objects.filter(issue__project__contributor_project__user=request.user).exists()

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update', 'destroy']:
            return obj.author.user == request.user
        return Comment.objects.filter(issue__project__contributor_project__user=request.user).exists()


