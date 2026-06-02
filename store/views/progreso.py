# store/views/progreso.py
from rest_framework import viewsets, permissions

from store.models import Progreso
from store.serializers import ProgresoSerializer


class ProgresoViewSet(viewsets.ModelViewSet):
    serializer_class   = ProgresoSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names  = ['get', 'post', 'patch', 'head', 'options']

    def get_queryset(self):
        user = self.request.user
        if user.rol == 'admin':
            return Progreso.objects.select_related('matricula', 'leccion').all()
        return Progreso.objects.select_related('matricula', 'leccion').filter(
            matricula__usuario=user
        )