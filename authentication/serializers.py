from rest_framework.serializers import ModelSerializer
from django.contrib.auth import authenticate, login, logout, get_user_model

User = get_user_model()


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'age', 'password', 'can_be_contacted', 'can_data_be_shared']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            age=validated_data['age'],
            can_be_contacted=validated_data['can_be_contacted'],
            can_data_be_shared=validated_data['can_data_be_shared']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

