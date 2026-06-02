# store/tests/test_usuario.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from store.models import Usuario


class RegistroTestCase(APITestCase):

    def test_registro_exitoso(self):
        data = {
            'username': 'estudiante1',
            'email':    'estudiante1@test.com',
            'password': 'clave1234',
            'rol':      'estudiante',
        }
        response = self.client.post(reverse('auth-registro'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Usuario.objects.count(), 1)

    def test_registro_sin_password_falla(self):
        data = {'username': 'test', 'email': 'test@test.com'}
        response = self.client.post(reverse('auth-registro'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registro_email_duplicado_falla(self):
        data = {'username': 'u1', 'email': 'dup@test.com', 'password': 'clave1234'}
        self.client.post(reverse('auth-registro'), data)
        data2 = {'username': 'u2', 'email': 'dup@test.com', 'password': 'clave1234'}
        response = self.client.post(reverse('auth-registro'), data2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTestCase(APITestCase):

    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='instructor1',
            email='instructor1@test.com',
            password='clave1234',
            rol='instructor',
        )

    def test_login_exitoso(self):
        data = {'username': 'instructor1', 'password': 'clave1234'}
        response = self.client.post(reverse('auth-login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access',  response.data)
        self.assertIn('refresh', response.data)

    def test_login_password_incorrecto(self):
        data = {'username': 'instructor1', 'password': 'incorrecta'}
        response = self.client.post(reverse('auth-login'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_perfil_me(self):
        self.client.force_authenticate(user=self.usuario)
        response = self.client.get('/api/usuarios/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'instructor1')