# store/tests/test_curso.py
from rest_framework import status
from rest_framework.test import APITestCase
from store.models import Usuario, Categoria, Curso


class CursoTestCase(APITestCase):

    def setUp(self):
        self.instructor = Usuario.objects.create_user(
            username='instructor1', password='clave1234', rol='instructor'
        )
        self.estudiante = Usuario.objects.create_user(
            username='estudiante1', password='clave1234', rol='estudiante'
        )
        self.categoria = Categoria.objects.create(nombre='Python', slug='python')
        self.curso = Curso.objects.create(
            titulo='Python básico',
            descripcion='Aprende Python',
            precio=29.99,
            nivel='basico',
            publicado=True,
            instructor=self.instructor,
            categoria=self.categoria,
        )

    def test_listar_cursos_publico(self):
        response = self.client.get('/api/cursos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detalle_curso_publico(self):
        response = self.client.get(f'/api/cursos/{self.curso.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['titulo'], 'Python básico')

    def test_crear_curso_instructor(self):
        self.client.force_authenticate(user=self.instructor)
        data = {
            'titulo':      'Django REST',
            'descripcion': 'API con Django',
            'precio':      '49.99',
            'nivel':       'intermedio',
            'publicado':   True,
            'categoria_id': self.categoria.id,
        }
        response = self.client.post('/api/cursos/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['instructor']['username'], 'instructor1')

    def test_crear_curso_estudiante_falla(self):
        self.client.force_authenticate(user=self.estudiante)
        data = {
            'titulo':      'Curso no permitido',
            'descripcion': 'Test',
            'precio':      '0',
            'nivel':       'basico',
            'categoria_id': self.categoria.id,
        }
        response = self.client.post('/api/cursos/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filtrar_por_nivel(self):
        response = self.client.get('/api/cursos/?nivel=basico')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for curso in response.data['results']:
            self.assertEqual(curso['nivel'], 'basico')