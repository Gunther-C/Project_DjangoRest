from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment

User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'type', 'author', 'date_joined']
        read_only_fields = ['author']


class ContributorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['id', 'project', 'user', 'role', 'created_date']
        read_only_fields = ['role']


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'project', 'author', 'assigned_to', 'priority',
                  'tag', 'status', 'created_time']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'description', 'issue', 'author', 'created_time']
