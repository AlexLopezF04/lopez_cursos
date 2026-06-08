from rest_framework import serializers
from store.models import Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Categoria
        fields = ['id', 'nombre', 'slug']
        extra_kwargs = {'slug': {'required': False}}