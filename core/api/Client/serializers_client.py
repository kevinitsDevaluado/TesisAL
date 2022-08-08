from rest_framework import serializers
from core.user.models import User
from core.pos.models import Client
from config import settings
from config.wsgi import *
from core.security.models import *
from django.contrib.auth.models import Permission
from core.pos.models import *



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("is_staff","date_joined","groups","user_permissions")

    def create(self,validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        group = Group.objects.get(pk=settings.GROUPS.get('client'))
        user.groups.add(group)
        return user

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields ="__all__"
