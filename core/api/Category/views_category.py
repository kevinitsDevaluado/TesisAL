from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets

from django.shortcuts import get_object_or_404

from core.pos.models import Category
from core.api.Category.serializers_category import CategorySerializer

class CategoryViewSet(viewsets.GenericViewSet):
    model = Category
    serializer_class = CategorySerializer

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.filter(activo=True)
        return self.queryset
    
    def list(self,request):
        category = self.get_queryset()
        if category:
            category_serializer = self.serializer_class(category,many=True)
            return Response(category_serializer.data, status = status.HTTP_200_OK)
        return Response( {"message":"No hay ninguna categoria"}, status=status.HTTP_400_BAD_REQUEST)