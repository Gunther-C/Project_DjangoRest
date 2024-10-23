from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Project, Contributor

User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'type', 'author', 'date_joined']
        read_only_fields = ['author', 'date_joined']


class ContributorSerializer(serializers.ModelSerializer):

    project_id = serializers.IntegerField(required=False, allow_null=True)
    project_name = serializers.CharField(max_length=255, required=False, allow_null=True)
    projects = Project.objects.all()
    project_list = serializers.CharField(max_length=255, choices=projects)

    class Meta:
        model = Contributor
        fields = ['project_id', 'project_name', 'project_list']
        read_only_fields = ['user', 'role']

