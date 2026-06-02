# store/views/curso.py
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from store.models import Curso
from store.serializers import CursoSerializer, CursoListSerializer
from store.pagination import StandardPagination
from store.permissions import EsInstructor, EsPropietarioOAdmin, EsSoloLectura


class CursoViewSet(viewsets.ModelViewSet):
    queryset         = Curso.objects.select_related('instructor', 'categoria').order_by('-created_at')
    pagination_class = StandardPagination
    filter_backends  = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['nivel', 'publicado', 'categoria']
    search_fields    = ['titulo', 'descripcion']
    ordering_fields  = ['precio', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return CursoListSerializer
        return CursoSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.AllowAny()]
        if self.action == 'create':
            return [permissions.IsAuthenticated(), EsInstructor()]
        return [permissions.IsAuthenticated(), EsPropietarioOAdmin()]

    def get_queryset(self):
        qs = super().get_queryset()
        # Usuarios no autenticados solo ven cursos publicados
        if not self.request.user.is_authenticated:
            return qs.filter(publicado=True)
        if self.request.user.rol == 'instructor':
            return qs.filter(publicado=True) | qs.filter(instructor=self.request.user)
        return qs

    @action(detail=True, methods=['get'], url_path='lecciones')
    def lecciones(self, request, pk=None):
        """GET /api/cursos/{id}/lecciones/"""
        from store.serializers import LeccionSerializer
        curso    = self.get_object()
        qs       = curso.lecciones.all()
        serializer = LeccionSerializer(qs, many=True)
        return Response(serializer.data)