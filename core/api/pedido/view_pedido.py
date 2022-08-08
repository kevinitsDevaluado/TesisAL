from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets

from django.shortcuts import get_object_or_404

from core.pos.models import Pedido
from core.api.pedido.serializers_pedido import PedidoSerializer,PedidoCreateSerializer
from core.pos.models import Sale, SaleDetail, Client, Product

class PedidoViewSet(viewsets.GenericViewSet):
    model = Pedido
    serializer_class = PedidoSerializer
    queryset = Pedido.objects.all()

    def list(self,request):
        pedidos_serializer = self.get_serializer(self.queryset, many=True)
        return Response(pedidos_serializer.data, status = status.HTTP_200_OK)


    def retrieve(self, request, pk=None):
        client = Client.objects.get(user_id = pk)
        pedido_client = self.model.objects.filter(client=client.id)
        if pedido_client:
            pedido_serializer = self.serializer_class(pedido_client, many=True)
            return Response(pedido_serializer.data, status = status.HTTP_200_OK)
        return Response({'message':'Pedidos del Cliente'}, status=status.HTTP_400_BAD_REQUEST)


    def create(self,request):
        pedidos_serializer = PedidoSerializer(data=request.data)
        pedido = request.data['pedido']  
        id_client = request.data['id_client']
        cliente  = Client.objects.get(user_id=id_client)
        print('Cliente id',cliente.id)

        if pedidos_serializer.is_valid():
            print(cliente.id)
            pedidos_serializer.save(client=cliente,activo=True)
            

            return Response({'message':'Pedido creado correctamente'}, status = status.HTTP_201_CREATED)
        return Response( pedidos_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_object(self,pk):
        return get_object_or_404(Pedido, id=pk)
    