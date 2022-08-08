from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets

from core.pos.models import Sale, SaleDetail, Client, Product, Company
from core.api.Sale.serializers_sale import SaleSerializer, PhotoSerializer


class SaleViewSet(viewsets.GenericViewSet):
    model = Sale
    serializer_class = SaleSerializer

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.all()
        return self.queryset
    
    def list(self,request):
        sale = self.get_queryset()
        if sale:
            sale_serializer = self.serializer_class(sale, many=True)
            return Response(sale_serializer.data, status = status.HTTP_200_OK)
        return Response({"message":"No hay ningun pedido"}, status = status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        action = request.GET.get('action')
        sale = Sale.objects.filter(client=pk,disponibilidad=action,estado=True).order_by('-id')
        
        if sale:
            sale_serializer = self.serializer_class(sale, many=True)
            return Response(sale_serializer.data, status= status.HTTP_200_OK)   
        return Response({'message':'No tiene ningun pedido'}, status = status.HTTP_400_BAD_REQUEST)

    # # verify orden
    def update(self,request,pk=None):
        sale_process = self.model.objects.filter(client=pk, estado=False).first()     
        if sale_process:
            id_client = Client.objects.filter(id=request.data['id_client']).first();
            image = request.data['image']
            total = request.data['total'] 

            comp = Company.objects.first()

            sale, created = Sale.objects.get_or_create(client=id_client,estado=False,disponibilidad=0)

            print(total, " ", sale.get_cart_total )
            
            if sale:

                if float(total) == float(sale.get_cart_total):
                    # update stock of school product
                    sale_product = SaleDetail.objects.filter(sale=sale.id)

                    print("-> ", sale_product)
                    
                    for product in sale_product:
                        print("Product -> ", product.product.id)
                        print("Product -> ", product)
                        productos = Product.objects.filter(id=product.product.id,activo=True).first()
                        print("Product -> ", productos)
                        if productos:
                            productos.stock = productos.stock - product.cant
                            productos.save()
                        else:
                            return Response({'message':'Lo sentimos a ocurrio un error intento de nuevo o más tarde 1'}, status = status.HTTP_400_BAD_REQUEST)  
                    
                    photo_serializer = PhotoSerializer(sale, data={'image':image})

                    if photo_serializer.is_valid():
                        photo_serializer.save()
                        sale.estado = True
                        sale.subtotal = sale.get_cart_total
                        sale.iva = comp.iva
                        sale.total_iva =  format(sale.get_cart_total * (comp.iva/100), '.2f')
                        total_finish = (sale.get_cart_total * (comp.iva/100)) + sale.get_cart_total
                        sale.total = format(total_finish, '.2f')
                        sale.cash = format(total_finish, '.2f')
                        sale.save()
                        return Response({'message':'Pedido realizado correctamente'}, status = status.HTTP_200_OK)
                    return Response(photo_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
                    # update sale
                    
                return Response({'message':'Lo sentimos a ocurrio un error intento de nuevo o más tarde XD', 'total':sale.get_cart_total,'items':sale.get_cart_items}, status = status.HTTP_400_BAD_REQUEST)

            return Response({'message':'No se encontro ninguna orden'}, status = status.HTTP_400_BAD_REQUEST)

        return Response({'message':'No se encontro ninguna orden'}, status = status.HTTP_400_BAD_REQUEST)


