# store/tests/test_resena.py
from rest_framework import status
from rest_framework.test import APITestCase
from store.models import Usuario, Categoria, Curso, Resena


class ResenaTestCase(APITestCase):

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

    def test_crear_resena(self):
        self.client.force_authenticate(user=self.estudiante)
        data = {
            'curso':        self.curso.id,
            'calificacion': 5,
            'comentario':   'Excelente curso',
        }
        response = self.client.post(f'/api/cursos/{self.curso.id}/resenas/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Resena.objects.count(), 1)

    def test_resena_duplicada_falla(self):
        self.client.force_authenticate(user=self.estudiante)
        data = {'curso': self.curso.id, 'calificacion': 4, 'comentario': 'Bueno'}
        self.client.post(f'/api/cursos/{self.curso.id}/resenas/', data)
        response = self.client.post(f'/api/cursos/{self.curso.id}/resenas/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_calificacion_fuera_de_rango_falla(self):
        self.client.force_authenticate(user=self.estudiante)
        data = {'curso': self.curso.id, 'calificacion': 6, 'comentario': 'Test'}
        response = self.client.post(f'/api/cursos/{self.curso.id}/resenas/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_listar_resenas_publico(self):
        response = self.client.get(f'/api/cursos/{self.curso.id}/resenas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)