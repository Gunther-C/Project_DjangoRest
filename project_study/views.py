from django.contrib.auth import get_user_model

from rest_framework import status, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .models import Project, Contributor
from .serializers import ProjectSerializer, AddContributorSerializer
from .permissions import IsAuthorOrReadOnly

User = get_user_model()


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Project.objects.filter(contributors__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

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


class AddContributorAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        project = Project.objects.get(id=pk)
        if request.user != project.author:
            return Response({"detail": "Vous n'êtes pas autorisé à ajouter des contributeurs à ce projet."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = AddContributorSerializer(data=request.data, context={'project': project})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_contributor(self, request, pk=None):
        project = self.get_object()
        if request.user != project.author:
            return Response({"detail": "Vous n'êtes pas autorisé à ajouter des contributeurs à ce projet."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = AddContributorSerializer(data=request.data, context={'project': project})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class CreateProjectAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ProjectSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""

