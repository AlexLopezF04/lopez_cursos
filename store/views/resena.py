# store/views/resena.py
from rest_framework import viewsets, permissions

from store.models import Resena 
from store.serializers import ResenaSerializer
from store.pagination import StandardPagination
from store.permissions import EsPropietarioOAdmin
from store.filters import ResenaFilter

class ResenaViewSet(viewsets.ModelViewSet):
    serializer_class   = ResenaSerializer
    pagination_class   = StandardPagination
    filterset_class = ResenaFilter
    permission_classes = [permissions.IsAuthenticated]
    http_method_names  = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        curso_pk = self.kwargs.get('curso_pk')
        if curso_pk:
            return Resena.objects.filter(curso__id=curso_pk).select_related('usuario')
        return Resena.objects.select_related('usuario', 'curso').filter(
            usuario=self.request.user
        )

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.AllowAny()]
        if self.action in ('update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated(), EsPropietarioOAdmin()]
        return super().get_permissions()