# store/models/curso.py
from django.db import models
from django.conf import settings

class Curso(models.Model):
    NIVEL_CHOICES = [
        ('basico',        'Básico'),
        ('intermedio',    'Intermedio'),
        ('avanzado',      'Avanzado'),
    ]
    instructor  = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cursos'
    )
    categoria   = models.ForeignKey(
        'Categoria', on_delete=models.SET_NULL, null=True, related_name='cursos'
    )
    titulo      = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio      = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    nivel       = models.CharField(max_length=20, choices=NIVEL_CHOICES, default='basico')
    publicado   = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo