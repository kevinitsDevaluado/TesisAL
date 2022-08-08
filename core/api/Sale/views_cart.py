from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets

from core.pos.models import Sale
from core.api.Sale.serializers_sale import CartSerializer


class CartViewSet(viewsets.GenericViewSet):
    model = Sale
    serializer_class = CartSerializer
# 
    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.all()
        return self.queryset
    
    def list(self,request):
        cart = self.get_queryset()
        if cart:
            cart_serializer = self.serializer_class(cart, many=True)
            return Response(cart_serializer.data, status = status.HTTP_200_OK)
        return Response({"message":"No hay ninguna pedido"}, status = status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self,request,pk=None):
        cart = self.model.objects.filter(client=pk, estado=False).first()
        if cart:
            cart_serializer = self.serializer_class(cart)
            return Response(cart_serializer.data, status = status.HTTP_200_OK)
        return Response({"message":"No hay ninguna pedido"}, status = status.HTTP_400_BAD_REQUEST)