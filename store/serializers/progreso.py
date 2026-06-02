from rest_framework import serializers
from store.models import Progreso
from django.utils import timezone

class ProgresoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Progreso
        fields = ['id', 'matricula', 'leccion', 'completada', 'fecha_completado']
        read_only_fields = ['fecha_completado']

    def update(self, instance, validated_data):
        if validated_data.get('completada') and not instance.completada:
            validated_data['fecha_completado'] = timezone.now()
        return super().update(instance, validated_data)