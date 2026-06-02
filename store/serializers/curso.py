from rest_framework import serializers
from store.models import Curso
from .usuario   import UsuarioSerializer
from .categoria import CategoriaSerializer

class CursoListSerializer(serializers.ModelSerializer):
    """Versión liviana para listados."""
    instructor = serializers.StringRelatedField()
    categoria  = serializers.StringRelatedField()

    class Meta:
        model  = Curso
        fields = ['id', 'titulo', 'nivel', 'precio', 'publicado', 'instructor', 'categoria']

class CursoSerializer(serializers.ModelSerializer):
    """Versión completa para detalle / creación."""
    instructor = UsuarioSerializer(read_only=True)
    categoria  = CategoriaSerializer(read_only=True)

    categoria_id  = serializers.PrimaryKeyRelatedField(
        source='categoria', queryset=__import__('store.models', fromlist=['Categoria']).Categoria.objects.all(),
        write_only=True
    )

    class Meta:
        model  = Curso
        fields = [
            'id', 'titulo', 'descripcion', 'precio', 'nivel',
            'publicado', 'instructor', 'categoria', 'categoria_id', 'created_at',
        ]
        read_only_fields = ['instructor', 'created_at']

    def create(self, validated_data):
        validated_data['instructor'] = self.context['request'].user
        return super().create(validated_data)