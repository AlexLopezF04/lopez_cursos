# store/tests/test_categoria.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from store.models import Usuario, Categoria


class CategoriaTestCase(APITestCase):

    def setUp(self):
        self.admin = Usuario.objects.create_user(
            username='admin1', password='clave1234', is_staff=True
        )
        self.estudiante = Usuario.objects.create_user(
            username='estudiante1', password='clave1234', rol='estudiante'
        )
        self.categoria = Categoria.objects.create(nombre='Programación', slug='programacion')

    def test_listar_categorias_publico(self):
        response = self.client.get('/api/categorias/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_crear_categoria_admin(self):
        self.client.force_authenticate(user=self.admin)
        data = {'nombre': 'Diseño', 'slug': 'diseno'}
        response = self.client.post('/api/categorias/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_crear_categoria_sin_permiso(self):
        self.client.force_authenticate(user=self.estudiante)
        data = {'nombre': 'Diseño', 'slug': 'diseno'}
        response = self.client.post('/api/categorias/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)