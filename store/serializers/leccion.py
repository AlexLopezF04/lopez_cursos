from rest_framework import serializers
from store.models import Leccion

class LeccionSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Leccion
        fields = ['id', 'curso', 'titulo', 'contenido', 'video_url', 'orden', 'duracion_min']
        read_only_fields = ['curso']