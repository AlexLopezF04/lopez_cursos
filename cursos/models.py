from django.db import models
from django.contrib.auth import get_user_model

# Obtenemos el modelo de usuario que configuraste en tu proyecto
User = get_user_model()

class Curso(models.Model):
    # 1. Información básica del curso
    nombre = models.CharField(
        max_length=150, 
        verbose_name="Nombre del Curso"
    )
    descripcion = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Descripción"
    )
    
    # 2. Relación: Cada curso pertenece a un creador/profesor (Usuario)
    # Si se borra el usuario, se borran sus cursos (on_delete=models.CASCADE)
    creador = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="cursos_creados",
        verbose_name="Creador/Profesor"
    )
    
    # 3. Fechas de control automáticas
    fecha_creacion = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Fecha de Creación"
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True, 
        verbose_name="Última Actualización"
    )
    
    # 4. Estado del curso (por si quieres ocultarlo temporalmente)
    activo = models.BooleanField(
        default=True, 
        verbose_name="¿Está Activo?"
    )

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ["-fecha_creacion"]  # Los más nuevos aparecen primero

    def __str__(self):
        return self.nombre

    # Reemplaza __ দেহে__ con __str__ (el corrector del sistema a veces altera esta palabra clave)
    def __str__(self):
        return self.nombre