from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Project, Contributor

User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'type', 'author', 'date_joined']
        read_only_fields = ['author', 'date_joined']


class AddContributorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    project_id = serializers.IntegerField(required=False, allow_null=True)
    project_name = serializers.CharField(max_length=255, required=False, allow_null=True)

    class Meta:
        model = Contributor
        fields = ['username', 'project_id', 'project_name']

    def validate(self, data):
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Utilisateur non trouvé.")
        data['user'] = user

        project_id = data.get('project_id')
        project_name = data.get('project_name')

        if project_id is not None:
            try:
                project = Project.objects.get(id=project_id)
            except Project.DoesNotExist:
                raise serializers.ValidationError("Projet non trouvé.")

        elif project_name:
            try:
                cleaned_project_name = " ".join(project_name.split())
                project = Project.objects.get(name__iexact=cleaned_project_name)
            except Project.DoesNotExist:
                raise serializers.ValidationError("Projet non trouvé.")

        else:
            raise serializers.ValidationError("Vous devez fournir soit l'ID soit le nom du projet.")

        data['project'] = project
        return data

    def create(self, validated_data):
        user = validated_data['user']
        project = validated_data['project']
        contributor, created = Contributor.objects.get_or_create(user=user, project=project,
                                                                 defaults={'role': 'contributor'})
        if not created:
            raise serializers.ValidationError("Projet non trouvé.")
        return contributor
