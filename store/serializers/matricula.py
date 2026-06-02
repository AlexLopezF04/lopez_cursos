# store/serializers/matricula.py
from rest_framework import serializers
from store.models import Matricula


class MatriculaSerializer(serializers.ModelSerializer):
    usuario_email = serializers.EmailField(source='usuario.email', read_only=True)
    curso_titulo  = serializers.CharField(source='curso.titulo',   read_only=True)

    class Meta:
        model  = Matricula
        fields = [
            'id', 'usuario', 'curso', 'usuario_email',
            'curso_titulo', 'fecha_pago', 'monto_pagado', 'estado',
        ]
        read_only_fields = ['usuario', 'fecha_pago']

    def validate(self, attrs):
        usuario = self.context['request'].user
        curso   = attrs.get('curso')
        if Matricula.objects.filter(usuario=usuario, curso=curso).exists():
            raise serializers.ValidationError('Ya estás matriculado en este curso.')
        return attrs

    def create(self, validated_data):
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)