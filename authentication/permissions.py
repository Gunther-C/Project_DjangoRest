from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission
# from .models import User
from django.contrib.auth import get_user_model
User = get_user_model()


class IsUser(BasePermission):
    """
    Permission personnalisée pour n'autoriser que les propriétaires d'un objet à y accéder
    et pour n'autoriser que l'utilisateur connecté à voir ses propres informations.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if view.action in ['list']:
            return User.objects.filter(pk=request.user.id).exists()

        return True

    def has_object_permission(self, request, view, obj):
        return obj == request.user



