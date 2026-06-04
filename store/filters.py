# store/filters.py
import django_filters
from store.models import Curso, Matricula, Resena


class CursoFilter(django_filters.FilterSet):
    """
    Filtros para el listado de cursos.
    Ejemplos de uso:
      ?nivel=basico
      ?publicado=true
      ?precio_min=10&precio_max=50
      ?categoria=1
      ?search=python        (manejado por SearchFilter en la vista)
    """
    precio_min = django_filters.NumberFilter(field_name='precio', lookup_expr='gte')
    precio_max = django_filters.NumberFilter(field_name='precio', lookup_expr='lte')

    class Meta:
        model   = Curso
        fields  = ['nivel', 'publicado', 'categoria', 'precio_min', 'precio_max']


class MatriculaFilter(django_filters.FilterSet):
    """
    Filtros para matrículas.
    Ejemplos de uso:
      ?estado=activa
      ?curso=3
      ?fecha_desde=2025-01-01&fecha_hasta=2025-12-31
    """
    fecha_desde = django_filters.DateTimeFilter(field_name='fecha_pago', lookup_expr='gte')
    fecha_hasta = django_filters.DateTimeFilter(field_name='fecha_pago', lookup_expr='lte')

    class Meta:
        model  = Matricula
        fields = ['estado', 'curso', 'fecha_desde', 'fecha_hasta']


class ResenaFilter(django_filters.FilterSet):
    """
    Filtros para reseñas.
    Ejemplos de uso:
      ?calificacion_min=4
      ?calificacion_max=5
      ?curso=2
    """
    calificacion_min = django_filters.NumberFilter(field_name='calificacion', lookup_expr='gte')
    calificacion_max = django_filters.NumberFilter(field_name='calificacion', lookup_expr='lte')

    class Meta:
        model  = Resena
        fields = ['curso', 'calificacion_min', 'calificacion_max']