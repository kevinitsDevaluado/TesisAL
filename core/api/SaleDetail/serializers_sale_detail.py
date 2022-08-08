from rest_framework import serializers
from core.pos.models import SaleDetail

class SaleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleDetail
        fields = "__all__"

    def to_representation(self,instance):
        return {
            'id' : instance.id,
            'id_sale':instance.sale.id,
            'id_product': instance.product.id,
            'name' : instance.product.name if instance.product is not None else "",
            'quantity' : instance.cant,
            'price' : instance.product.get_price_discount if instance.product is not None else "",
            'image' : instance.product.image.url if instance.product is not None else "",
            'total' : instance.sale.total if instance.sale is not None else ""
        }

class SaleDetailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleDetail
        exclude = ("sale","product")


class SaleUpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleDetail
        fields = ("cant",)