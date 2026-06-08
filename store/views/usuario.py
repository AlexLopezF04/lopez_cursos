# store/views/usuario.py
from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from store.models import Usuario
from store.serializers import UsuarioSerializer, UsuarioCreateSerializer
from store.pagination import StandardPagination
from store.permissions import EsAdminDjango, EsPropietarioOAdmin


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Retorna tokens + datos del usuario al hacer login."""

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data.update({
            'user_id':  user.id,
            'username': user.username,
            'email':    user.email,
            'rol':      user.rol,
        })
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegistroView(generics.CreateAPIView):
    """POST /api/auth/registro/ — público. Retorna tokens + datos del usuario."""
    queryset         = Usuario.objects.all()
    serializer_class = UsuarioCreateSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'access':   str(refresh.access_token),
            'refresh':  str(refresh),
            'user_id':  user.id,
            'username': user.username,
            'email':    user.email,
            'rol':      user.rol,
        }, status=status.HTTP_201_CREATED)


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