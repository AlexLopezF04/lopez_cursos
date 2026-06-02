# store/models/progreso.py
from django.db import models

class Progreso(models.Model):
    matricula        = models.ForeignKey('Matricula', on_delete=models.CASCADE, related_name='progresos')
    leccion          = models.ForeignKey('Leccion',   on_delete=models.CASCADE, related_name='progresos')
    completada       = models.BooleanField(default=False)
    fecha_completado = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('matricula', 'leccion')

    def __str__(self):
        estado = '✓' if self.completada else '○'
        return f"{estado} {self.matricula} | {self.leccion}"