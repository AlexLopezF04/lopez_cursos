# store/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS


class EsSoloLectura(BasePermission):
    """Permite GET, HEAD, OPTIONS a cualquiera."""
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class EsInstructor(BasePermission):
    """Solo usuarios con rol instructor o admin."""
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.rol in ('instructor', 'admin')
        )


class EsPropietarioOAdmin(BasePermission):
    """Permite editar solo al dueño del objeto o un admin."""
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.rol == 'admin':
            return True
        propietario = getattr(obj, 'instructor', None) or getattr(obj, 'usuario', None)
        return propietario == request.user


class EsAdminDjango(BasePermission):
    """Solo staff de Django o rol admin."""
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.is_staff or request.user.rol == 'admin')
        )