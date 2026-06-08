# store/serializers/resena.py
from rest_framework import serializers
from store.models import Resena, Matricula


class ResenaSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model  = Resena
        fields = ['id', 'usuario', 'curso', 'usuario_nombre', 'calificacion', 'comentario', 'created_at']
        read_only_fields = ['usuario', 'created_at']

    def validate(self, attrs):
        usuario = self.context['request'].user
        curso   = attrs.get('curso')
        if not curso:
            return attrs
        if Resena.objects.filter(usuario=usuario, curso=curso).exists():
            raise serializers.ValidationError('Ya dejaste una reseña para este curso.')
        if not Matricula.objects.filter(usuario=usuario, curso=curso, estado='activa').exists():
            raise serializers.ValidationError('Debes estar matriculado activamente para dejar una reseña.')
        return attrs

    def create(self, validated_data):
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)