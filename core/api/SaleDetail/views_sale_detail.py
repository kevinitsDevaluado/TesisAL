from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets

from django.shortcuts import get_object_or_404

from core.pos.models import Sale, SaleDetail, Client, Product
from core.api.SaleDetail.serializers_sale_detail import SaleDetailSerializer,SaleUpdateProductSerializer,SaleDetailCreateSerializer

class SaleDetailViewSet(viewsets.GenericViewSet):
    model = SaleDetail
    serializer_class = SaleDetailSerializer

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.all()
        return self.queryset
    
    def list(self,request):
        sale_product = self.get_queryset()
        sale_product_serializer = self.serializer_class(sale_product, many=True)
        return Response(sale_product_serializer.data, status= status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):

        action = request.GET.get('action')
        id_order = request.GET.get('id','')
        client = Client.objects.get(user_id = pk)

        if action=="card":
            sale = Sale.objects.filter(client=client.id).first()
        else:
            sale = Sale.objects.filter(client=pk,id=id_order).first()

        if sale:
            sale_product = self.model.objects.filter(sale=sale.id) 
            if sale_product:
                sale_product_serializer = self.serializer_class(sale_product, many=True)
                return Response(sale_product_serializer.data, status= status.HTTP_200_OK)
            return Response({'message':'No tienes productos en el carrito'}, status = status.HTTP_400_BAD_REQUEST)
        return Response({'message':'No tienes productos en el carrito erro|'}, status = status.HTTP_400_BAD_REQUEST)
    
    def create(self,request):
       
        sale_product = SaleDetailCreateSerializer(data=request.data)

        if sale_product.is_valid():

            id_client = Client.objects.filter(id=request.data['id_client']).first();
            sale_specifity_quantity = request.data['quantity']  
            id_product = request.data['id_product']
            action = request.data['action']

            sale, created = Sale.objects.get_or_create(client=id_client,estado=False,disponibilidad=0)
       
            if action=="create_update":
                
                verify_order = self.model.objects.filter(sale=sale.id).first()
                if verify_order:
                    # update
                    verify_product = self.model.objects.filter(sale=sale.id,product=id_product).first()
                    if verify_product:
                        # verify quantity in school product
                        product = Product.objects.filter(id=id_product).first()
                        if product:
                            if product.stock > verify_product.cant:
                        
                                if ((verify_product.cant+int(sale_specifity_quantity)) <= product.stock) :
                                    verify_product.cant = verify_product.cant+int(sale_specifity_quantity)
                                    sale_update_product = SaleUpdateProductSerializer(verify_product, data={'cant':verify_product.cant})
                                    if sale_update_product.is_valid():
                                        sale_update_product.save()
                                        return Response({'message':'La cantidad fue actualizada correctamente'}, status = status.HTTP_200_OK)
                                    return Response(sale_update_product.errors, status=status.HTTP_400_BAD_REQUEST)
                                
                                if verify_product.cant+int(sale_specifity_quantity) > product.stock:
                                    return Response({'message':'Lo sentimos no disponemos de esa cantidad en el producto'}, status = status.HTTP_400_BAD_REQUEST)
                                else:
                                    return Response({'message':'Lo sentimos no disponemos de esa cantidad en el producto'}, status = status.HTTP_400_BAD_REQUEST)

                            sale_update_product = SaleUpdateProductSerializer(verify_product, data={'cant':product.stock})
                            if sale_update_product.is_valid():
                                sale_update_product.save()
                                return Response({'message':'Lo sentimos no disponemos de esa cantidad en el producto'}, status = status.HTTP_400_BAD_REQUEST)
                            return Response(sale_update_product.errors, status=status.HTTP_400_BAD_REQUEST)

                        return Response({'message':'Lo sentimos el producto no se encuentra disponible'}, status = status.HTTP_400_BAD_REQUEST)
                
                # create
                product = Product.objects.filter(id=id_product).first()
                if product:
                    if product.stock>0:
                        saledetail, created = SaleDetail.objects.get_or_create(sale=sale, product=product, cant=sale_specifity_quantity)
                        return Response({'message':'Detalle de la orden creada correctamente'}, status = status.HTTP_200_OK)
                    return Response({'message':'Lo sentimos el producto no se encuentra disponible'}, status = status.HTTP_400_BAD_REQUEST)   
                return Response({'message':'Lo sentimos el producto no se encuentra disponible'}, status = status.HTTP_400_BAD_REQUEST)   
            
            if action=="add":
                # verify order in order school product
                verify_order = self.model.objects.filter(sale=sale.id).first()
                if verify_order:
                    # verify school product
                    verify_product = self.model.objects.filter(sale=sale.id,product=id_product).first()
                    if verify_product:
                        # verify quantity in school product
                        product = Product.objects.filter(id=id_product).first()
                        if product:
                            if product.stock > verify_product.cant:

                                # if verify_product.cant < 10:
                                verify_product.cant = verify_product.cant+1
                                sale_update_product = SaleUpdateProductSerializer(verify_product, data={'cant':verify_product.cant})
                                if sale_update_product.is_valid():
                                    sale_update_product.save()
                                    return Response({'message':'La cantidad fue actualizada correctamente'}, status = status.HTTP_200_OK)
                                return Response(sale_update_product.errors, status=status.HTTP_400_BAD_REQUEST)


                            sale_update_product = SaleUpdateProductSerializer(verify_product, data={'cant':product.stock})
                            if sale_update_product.is_valid():
                                sale_update_product.save()
                                return Response({'message':'Lo sentimos no disponemos de esa cantidad en el producto'}, status = status.HTTP_400_BAD_REQUEST)
                            return Response(sale_update_product.errors, status=status.HTTP_400_BAD_REQUEST)

                        return Response({'message':'Lo sentimos el producto no se encuentra disponible'}, status = status.HTTP_400_BAD_REQUEST)

                return Response({'message':'Lo sentimos el producto no se encuentra disponible'}, status = status.HTTP_400_BAD_REQUEST)

            if action=="remove":
                # 
                verify_order = self.model.objects.filter(sale=sale.id).first()
                if verify_order:
                    # verify school product
                    verify_product = self.model.objects.filter(sale=sale.id,product=id_product).first()
                    if verify_product:
                        product = Product.objects.filter(id=id_product).first()
                        if product:
                            if product.stock > verify_product.cant: 
                                if verify_product.cant == 1:
                                    verify_product.delete()
                                else:
                                    verify_product.cant = verify_product.cant-1
                                    sale_update_product = SaleUpdateProductSerializer(verify_product, data={'cant':verify_product.cant})
                                    if sale_update_product.is_valid():
                                        sale_update_product.save()
                                        return Response({'message':'La cantidad fue actualizada correctamente'}, status = status.HTTP_200_OK)
                                    return Response(sale_update_product.errors, status=status.HTTP_400_BAD_REQUEST)
                                return Response({'message':'El producto fue eliminado correctamente'}, status = status.HTTP_200_OK)

                            sale_update_product = SaleUpdateProductSerializer(verify_product, data={'cant':product.stock-1})
                            if sale_update_product.is_valid():
                                sale_update_product.save()
                                print("Cantidad : ", product.stock-1 )
                                return Response({'message':'La cantidad fue actualizada correctamente'}, status = status.HTTP_200_OK)
                            return Response(sale_update_product.errors, status=status.HTTP_400_BAD_REQUEST)

                        return Response({'message':'1 Lo sentimos el producto no se encuentra disponible'}, status = status.HTTP_400_BAD_REQUEST)
                
                return Response({'message':'2 Lo sentimos el producto no se encuentra disponible'}, status = status.HTTP_400_BAD_REQUEST)
            
               
        return Response( sale_product.errors, status=status.HTTP_400_BAD_REQUEST)