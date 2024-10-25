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
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Contributor
        fields = ['project', 'user', 'role', 'created_date']
        read_only_fields = ['user', 'role', 'created_date']
