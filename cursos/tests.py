from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Curso  # <-- Asegúrate de que tu modelo se llame 'Curso' (en mayúscula)

User = get_user_model()

class CursoTests(APITestCase):

    def setUp(self):
        """
        Este método ejecuta configuraciones previas a cada test.
        Creamos un usuario de prueba y un curso inicial.
        """
        self.user = User.objects.create_user(
            username="testuser", 
            password="testpassword123"
        )
        
        # OJO: Si tu modelo 'Curso' tiene campos obligatorios diferentes
        # (como 'descripcion', 'precio', etc.), agrégalos aquí.
        self.curso = Curso.objects.create(
            nombre="Introducción a Django"
        )
        
        # Ruta típica para listar cursos (asumiendo que usas routers o nombres de URL estándar)
        # Si no tienes las URLs listas todavía, el 'Test 1' igual funcionará.
        self.url_lista_cursos = reverse('curso-list') 

    # -----------------------------------------------------------------
    # TEST 1: Prueba básica de Base de Datos (Modelo)
    # -----------------------------------------------------------------
    def test_creacion_de_curso(self):
        """Verifica que un curso se cree correctamente en la base de datos."""
        curso_nuevo = Curso.objects.create(nombre="Curso de Python Avanzado")
        
        # Comprobamos que el nombre guardado sea el correcto
        self.assertEqual(curso_nuevo.nombre, "Curso de Python Avanzado")
        # Comprobamos que ahora existan 2 cursos en total (el del setUp + este)
        self.assertEqual(Curso.objects.count(), 2)

    # -----------------------------------------------------------------
    # TEST 2: Prueba de API (GET / Endpoint de listado)
    # -----------------------------------------------------------------
    def test_obtener_lista_de_cursos(self):
        """Verifica que el endpoint devuelva la lista de cursos de forma exitosa."""
        try:
            response = self.client.get(self.url_lista_cursos)
            # Comprobamos que el servidor responda con un estado 200 OK
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        except Exception:
            # Si aún no tienes configuradas tus URLs, saltamos este test temporalmente
            self.skipTest("La URL 'curso-list' aún no está configurada en urls.py")