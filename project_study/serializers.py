from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment

User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'type', 'author', 'created_date']
        read_only_fields = ['author']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['author'] = instance.author.username
        return ret


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'project', 'user', 'role', 'created_date']
        read_only_fields = ['role']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['project'] = instance.project.name
        ret['user'] = instance.user.username
        return ret


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'project', 'author', 'assigned_to', 'priority',
                  'tag', 'status', 'created_date']
        read_only_fields = ['author']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['project'] = instance.project.name
        ret['author'] = instance.author.user.username
        ret['assigned_to'] = {
            "name": instance.assigned_to.user.username,
            "role": instance.assigned_to.role
        } if instance.assigned_to else None
        return ret


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'description', 'issue', 'created_date']
        read_only_fields = ['id', 'author', 'created_date']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['author'] = instance.author.user.username
        ret['issue'] = {
            "author": instance.issue.author.user.username,
            "projet": instance.issue.project.name,
            "title": instance.issue.title,
            "priority": instance.issue.priority,
            "tag": instance.issue.tag,
            "status": instance.issue.status,
            "date": instance.issue.created_date,
        }
        return ret
