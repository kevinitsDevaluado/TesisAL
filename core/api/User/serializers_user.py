from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.user.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class UserTokenSerializerJWT(TokenObtainPairSerializer):
    pass

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','first_name','last_name')
