from rest_framework.permissions import BasePermission
from .models import Contributor


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.metod in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return True
        return Contributor.objects.filter(user=request.user, project=obj, role='author').exists()


class IsContributor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return Contributor.objects.filter(user=request.user, project=obj, role='contributor').exists()


class IsContributorOrAuthor(BasePermission):

    """def has_permission(self, request, view):
        return Contributor.objects.filter(user=request.user, project=obj, role='contributor').exists()"""

    def has_object_permission(self, request, view, obj):
        if request.method == 'PATCH' or request.method == 'DELETE':
            return Contributor.objects.filter(user=request.user, project=obj, role='author').exists()


