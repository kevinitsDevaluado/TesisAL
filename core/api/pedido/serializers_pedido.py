from rest_framework import serializers
from core.pos.models import Pedido

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
        # exclude = ("is_staff","date_joined","groups","user_permissions")



class PedidoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        exclude = ("activo")