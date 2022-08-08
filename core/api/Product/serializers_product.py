from rest_framework import serializers
from core.pos.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def to_representation(self,instance):
        return {
            'id' : instance.id,
            'name' : instance.name,
            'stock' : instance.stock,
            'pvp' : instance.pvp,
            'image' : instance.image.url,
            'iva' : instance.iva,
            'activo' : instance.activo,
            'category' : instance.category.id if instance.category is not None else "",
            'price_get_discount' : instance.get_discount,
            'price_discount' : instance.get_price_discount
        }