# store/views/usuario.py
from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from store.models import Usuario
from store.serializers import UsuarioSerializer, UsuarioCreateSerializer
from store.pagination import StandardPagination
from store.permissions import EsAdminDjango, EsPropietarioOAdmin


class RegistroView(generics.CreateAPIView):
    """POST /api/auth/registro/ — público."""
    queryset         = Usuario.objects.all()
    serializer_class = UsuarioCreateSerializer
    permission_classes = [permissions.AllowAny]


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset           = Usuario.objects.all().order_by('id')
    serializer_class   = UsuarioSerializer
    pagination_class   = StandardPagination
    permission_classes = [permissions.IsAuthenticated, EsPropietarioOAdmin]

    def get_permissions(self):
        if self.action == 'list':
            return [EsAdminDjango()]
        return super().get_permissions()

    @action(detail=False, methods=['get', 'patch'], url_path='me')
    def me(self, request):
        """GET /api/usuarios/me/ — perfil del usuario autenticado."""
        if request.method == 'PATCH':
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response(self.get_serializer(request.user).data)