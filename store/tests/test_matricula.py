# store/tests/test_matricula.py
from rest_framework import status
from rest_framework.test import APITestCase
from store.models import Usuario, Categoria, Curso, Matricula


class MatriculaTestCase(APITestCase):

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

    def test_matricularse(self):
        self.client.force_authenticate(user=self.estudiante)
        data = {'curso': self.curso.id, 'monto_pagado': '29.99'}
        response = self.client.post('/api/matriculas/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Matricula.objects.count(), 1)

    def test_matricula_duplicada_falla(self):
        self.client.force_authenticate(user=self.estudiante)
        data = {'curso': self.curso.id, 'monto_pagado': '29.99'}
        self.client.post('/api/matriculas/', data)
        response = self.client.post('/api/matriculas/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_estudiante_ve_solo_sus_matriculas(self):
        otro = Usuario.objects.create_user(
            username='estudiante2', password='clave1234', rol='estudiante'
        )
        Matricula.objects.create(
            usuario=otro, curso=self.curso, monto_pagado=29.99
        )
        self.client.force_authenticate(user=self.estudiante)
        response = self.client.get('/api/matriculas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)