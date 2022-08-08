from rest_framework import serializers
from core.pos.models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        # exclude = ("is_staff","date_joined","groups","user_permissions")