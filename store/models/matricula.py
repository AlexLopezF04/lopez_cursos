# store/models/matricula.py
from django.db import models
from django.conf import settings

class Matricula(models.Model):
    ESTADO_CHOICES = [
        ('activa',    'Activa'),
        ('vencida',   'Vencida'),
        ('cancelada', 'Cancelada'),
    ]
    usuario      = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='matriculas'
    )
    curso        = models.ForeignKey(
        'Curso', on_delete=models.CASCADE, related_name='matriculas'
    )
    fecha_pago   = models.DateTimeField(auto_now_add=True)
    monto_pagado = models.DecimalField(max_digits=8, decimal_places=2)
    estado       = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activa')

    class Meta:
        unique_together = ('usuario', 'curso')
        ordering = ['-fecha_pago']

    def __str__(self):
        return f"{self.usuario} → {self.curso}"