from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'age', 'password', 'can_be_contacted', 'can_data_be_shared']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'label': 'Nom d\'usage'},
            'can_be_contacted': {'label': 'Peut ètre contacté'},
            'can_data_be_shared': {'label': 'Les données peuvent être partagées'}
        }

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


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise AuthenticationFailed('Impossible de s\'authentifier avec les informations fournies.')
        else:
            raise serializers.ValidationError('Tous les champs sont requis.')

        data['user'] = user
        return data


