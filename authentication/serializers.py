from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'age', 'password', 'can_be_contacted', 'can_data_be_shared']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'label': 'Nom d\'usage'},
            'can_be_contacted': {'label': 'Peut ètre contacté'},
            'can_data_be_shared': {'label': 'Les données peuvent être partagées'}
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if not user:
                raise AuthenticationFailed('Impossible de s\'authentifier avec les informations fournies.')
        else:
            raise serializers.ValidationError('Tous les champs sont requis.')

        data['user'] = user
        return data
