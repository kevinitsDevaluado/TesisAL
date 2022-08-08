from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from core.user.models import User
from core.pos.models import *
from core.api.User.serializers_user import UserSerializer,UserTokenSerializerJWT,CustomUserSerializer

class UserViewSet(viewsets.GenericViewSet):
    model = User
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.all()
        return self.queryset
    
    def list(self,request):
        user = self.get_queryset()
        if user:
            user_serializer = self.serializer_class(user,many=True)
            return Response(user_serializer.data, status = status.HTTP_200_OK)
        return Response({"message":"No hay ninguna usuario"}, status = status.HTTP_400_BAD_REQUEST)


class Login(TokenObtainPairView):
    serializer_class = UserTokenSerializerJWT

    def post(self, request , *args, **kwargs):
        username = request.data.get('username','')
        password = request.data.get('password', '')
        user = authenticate(
            username=username,
            password=password
        )

        if user:
            if user.is_active:
                print('EMAIL',user.email)
                print('id',user.id)
                login_serializer = self.serializer_class(data=request.data)
                if login_serializer.is_valid():
                    user_serializer = CustomUserSerializer(user)
                    arrayUser = [user_serializer.data]

                    get_client_id = Client.objects.filter(user=user.id)
                    for cli in get_client_id:
                        client_id = cli.id

                    return Response({
                        'token': login_serializer.validated_data.get('access'),
                        'refresh_token': login_serializer.validated_data.get('refresh'),
                        'user': arrayUser,
                        'id_client': user.id,
                        'message': 'Inicio de sesión Exitoso'
                    }, status= status.HTTP_200_OK)

                return Response({'message': 'Contraseña o nombre de usuario incorrecto'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'Cuenta desabilitada'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'message': 'Contraseña o nombre de usuario incorrecto'}, status=status.HTTP_400_BAD_REQUEST)

class Logout(GenericAPIView):
    def post(self, request , *args, **kwargs):
        # recibimos el id
        user = User.objects.filter(id=request.data.get('user',0))
        if user.exists():
            RefreshToken.for_user(user.first())
            return Response({'message': 'Sesión cerrada correctamente'},status= status.HTTP_200_OK)
        return Response({'error': 'No existe este usuario'}, status=status.HTTP_400_BAD_REQUEST)