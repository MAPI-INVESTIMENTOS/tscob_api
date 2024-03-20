from rest_framework import serializers,generics,permissions
from django.contrib.auth.models import User
from .models import *

class Empresa_Serializado(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user

class Pedido_Quitacao_Serializado(serializers.ModelSerializer):
    class Meta:
        model=Pedidos_Quitacao
        fields = '__all__'

class Quitacao_Serializado(serializers.ModelSerializer):
    class Meta:
        model=Quitacao
        fields="__all__"


class Empresa_Quitacao_Serializado(serializers.ModelSerializer):
    class Meta:
        model=Empresa_Quitacao
        fields="__all__"

class Empresa_Atencedentes_Serializado(serializers.ModelSerializer):
    class Meta:
        model = Empresa_Atencedentes
        fields = "__all__"