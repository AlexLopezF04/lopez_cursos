# store/models/usuario.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROL_CHOICES = [
        ('estudiante', 'Estudiante'),
        ('instructor', 'Instructor'),
        ('admin',      'Administrador'),
    ]
    rol        = models.CharField(max_length=20, choices=ROL_CHOICES, default='estudiante')
    bio        = models.TextField(blank=True)
    foto       = models.ImageField(upload_to='usuarios/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email