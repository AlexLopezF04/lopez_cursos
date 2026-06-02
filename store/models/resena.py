# store/models/resena.py
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Resena(models.Model):
    usuario      = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resenas'
    )
    curso        = models.ForeignKey(
        'Curso', on_delete=models.CASCADE, related_name='resenas'
    )
    calificacion = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comentario   = models.TextField(blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'curso')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.usuario} → {self.curso} ({self.calificacion}★)"