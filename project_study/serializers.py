from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Project

User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['name', 'type', 'description']

    """def create(self, validated_data):
        project = Project(
            name=validated_data['name'],
            type=validated_data['type'],
            description=validated_data['description']
        )
        project.save()
        return project"""
