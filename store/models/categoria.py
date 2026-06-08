# store/models/categoria.py
from django.db import models
from django.core.validators import RegexValidator

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug   = models.CharField(
        max_length=100,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[a-zA-Z0-9áéíóúüñÁÉÍÓÚÜÑ\s\-_,.]+$',
            message='El slug solo puede contener letras, números, espacios, guiones, guiones bajos, comas y puntos.',
        )],
    )

    def __str__(self):
        return self.nombre