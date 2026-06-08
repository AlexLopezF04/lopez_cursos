# store/serializers/usuario.py
from rest_framework import serializers
from store.models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'rol', 'is_staff', 'bio', 'foto', 'created_at']
        read_only_fields = ['created_at']


class UsuarioCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model  = Usuario
        fields = ['username', 'email', 'password', 'rol']

    def validate_email(self, value):
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError('Ya existe un usuario con este email.')
        return value

    def create(self, validated_data):
        return Usuario.objects.create_user(**validated_data)