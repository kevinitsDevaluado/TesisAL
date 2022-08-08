from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets

from django.shortcuts import get_object_or_404

from core.user.models import User
from core.pos.models import Client
from core.api.Client.serializers_client import UserSerializer, ClientSerializer

class ClientViewSet(viewsets.GenericViewSet):
    model = User
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def list(self,request):
        users_serializer = self.get_serializer(self.queryset, many=True)
        return Response(users_serializer.data, status = status.HTTP_200_OK)

    def create(self,request):
        users_serializer = UserSerializer(data=request.data)
        if users_serializer.is_valid():
            users_serializer.save()
            id_cli = User.objects.get(id = users_serializer.data['id'])
            mobile = request.data['mobile']
            address = request.data['address']
            Client.objects.create(user=id_cli,mobile=mobile,address=address)
            return Response({'message':'Usuario creado correctamente'}, status = status.HTTP_201_CREATED)
        return Response( users_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_object(self,pk):
        return get_object_or_404(Client, id=pk)
    
    def retrieve(self, request, pk=None):
        user = self.get_object(pk)
        user_serializer = ClientSerializer(user)
        return Response([user_serializer.data], status = status.HTTP_200_OK)
    