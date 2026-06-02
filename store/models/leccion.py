# store/models/leccion.py
from django.db import models

class Leccion(models.Model):
    curso        = models.ForeignKey('Curso', on_delete=models.CASCADE, related_name='lecciones')
    titulo       = models.CharField(max_length=200)
    contenido    = models.TextField(blank=True)
    video_url    = models.URLField(blank=True)
    orden        = models.PositiveIntegerField(default=0)
    duracion_min = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"{self.curso} — {self.titulo}"