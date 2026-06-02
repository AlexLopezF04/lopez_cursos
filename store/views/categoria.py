# store/views/categoria.py
from rest_framework import viewsets, permissions

from store.models import Categoria
from store.serializers import CategoriaSerializer
from store.permissions import EsAdminDjango, EsSoloLectura


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset           = Categoria.objects.all().order_by('nombre')
    serializer_class   = CategoriaSerializer
    permission_classes = [EsSoloLectura | EsAdminDjango]