from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets

from django.shortcuts import get_object_or_404

from core.pos.models import Product
from core.api.Product.serializers_product import ProductSerializer

class ProductViewSet(viewsets.GenericViewSet):
    model = Product
    serializer_class = ProductSerializer
    
    def list(self,request):
        product = self.get_queryset()
        if product:
            product_serializer = self.serializer_class(product,many=True)
            return Response(product_serializer.data, status = status.HTTP_200_OK)
        return Response( {"message":"No hay ningun producto"}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        product_category = self.model.objects.filter(category=pk)
        if product_category:
            product_category_serializer = self.serializer_class(product_category, many=True)
            return Response(product_category_serializer.data, status = status.HTTP_200_OK)
        return Response({'message':'No se a encontrado ningun producto en esta categoria'}, status=status.HTTP_400_BAD_REQUEST)

    