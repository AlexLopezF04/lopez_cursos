# store/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from store.models import Usuario, Categoria, Curso, Leccion, Matricula, Progreso, Resena


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display  = ['username', 'email', 'rol', 'is_staff']
    list_filter   = ['rol', 'is_staff']
    fieldsets     = UserAdmin.fieldsets + (
        ('Datos extra', {'fields': ('rol', 'bio', 'foto')}),
    )


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'slug']
    prepopulated_fields = {'slug': ('nombre',)}


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display  = ['titulo', 'instructor', 'categoria', 'nivel', 'precio', 'publicado']
    list_filter   = ['nivel', 'publicado', 'categoria']
    search_fields = ['titulo', 'descripcion']


@admin.register(Leccion)
class LeccionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'curso', 'orden', 'duracion_min']
    list_filter  = ['curso']


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'curso', 'estado', 'monto_pagado', 'fecha_pago']
    list_filter  = ['estado']


@admin.register(Progreso)
class ProgresoAdmin(admin.ModelAdmin):
    list_display = ['matricula', 'leccion', 'completada', 'fecha_completado']
    list_filter  = ['completada']


@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'curso', 'calificacion', 'created_at']
    list_filter  = ['calificacion']