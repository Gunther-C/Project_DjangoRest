from django.contrib.auth import get_user_model
from rest_framework.decorators import action

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, LoginSerializer

User = get_user_model()


class RegisterApiView(APIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            user = User(
                username=validated_data.get('username'),
                age=validated_data.get('age'),
                can_be_contacted=validated_data.get('can_be_contacted'),
                can_data_be_shared=validated_data.get('can_data_be_shared')
            )
            user.set_password(validated_data.get('password'))
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""class UserProfileViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    @action(detail=False, methods=['patch'])
    def update_profile(self, request):
        serializer = RegisterSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        user = self.get_object()
        return serializer.save(user)"""


class UserProfileViewSet(ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request):
        user = request.user
        serializer = RegisterSerializer(user)
        return Response(serializer.data)

    def update(self, request):
        user = request.user
        serializer = RegisterSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)












