from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from core.pos.models import Sale

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        # fields = "__all__"
        exclude = ("end_credit",)
    
    def to_representation(self,instance):
        return {
            'id' : instance.id,
            'estado' : instance.estado,
            'disponibilidad' : instance.disponibilidad,
            'image' : instance.image.url if instance.image else "",
            'date':instance.date_joined,
            'items' : instance.get_cart_items,
            'total_cart': instance.get_cart_total
        }

class PhotoSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)
    class Meta:
        model = Sale
        fields = ("image",)

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model= Sale
        fields = "__all__"
        # exclude = ("created_in","updated_in")
    
    def to_representation(self,instance):
        return {
            'id' : instance.id,
            'estado' : instance.estado,
            'disponibilidad' : instance.disponibilidad,
            'user' : instance.client.user.username if instance.client is not None else "",
            'items' : instance.get_cart_items,
            'total_cart': instance.get_cart_total
        }
