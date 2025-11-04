from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User

class AuthTests(APITestCase):
    """
    Suite de pruebas para el módulo de Autenticación y Registro de Usuarios.
    """

    def setUp(self):
        # Este método se ejecuta antes de cada prueba.
        # Definimos las URLs que vamos a probar.
        self.register_url = reverse('auth_register')
        self.login_url = reverse('token_obtain_pair')

        # Datos de prueba para un usuario válido
        self.valid_user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'StrongPassword123',
            'password2': 'StrongPassword123'
        }

        # Datos de prueba para un usuario con contraseñas que no coinciden
        self.mismatched_password_data = {
            'username': 'testuser2',
            'email': 'test2@example.com',
            'password': 'StrongPassword123',
            'password2': 'WrongPassword'
        }

    # --- Pruebas para el Endpoint de Registro ---

    def test_registro_exitoso(self):
        """
        Verifica que un usuario puede registrarse exitosamente con datos válidos.
        Esto prueba el "camino feliz" del Caso de Uso CU-01.
        """
        # Hacemos una petición POST a la URL de registro
        response = self.client.post(self.register_url, self.valid_user_data, format='json')

        # Verificamos que la respuesta tenga el código de estado 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verificamos que el usuario se haya creado en la base de datos
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_registro_contraseñas_no_coinciden(self):
        """
        Verifica que el sistema devuelve un error si las contraseñas no coinciden.
        Esto prueba un "flujo alternativo" del Caso de Uso CU-01.
        """
        response = self.client.post(self.register_url, self.mismatched_password_data, format='json')

        # Verificamos que la respuesta sea un error 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Verificamos que no se haya creado ningún usuario
        self.assertEqual(User.objects.count(), 0)

    # --- Pruebas para el Endpoint de Inicio de Sesión ---

    def test_inicio_sesion_exitoso(self):
        """
        Verifica que un usuario registrado puede iniciar sesión correctamente.
        Esto prueba el "camino feliz" del Caso de Uso CU-02.
        """
        # Primero, creamos un usuario con el que vamos a intentar iniciar sesión
        self.client.post(self.register_url, self.valid_user_data, format='json')

        login_data = {
            'username': 'testuser',
            'password': 'StrongPassword123'
        }
        # Hacemos la petición POST a la URL de login
        response = self.client.post(self.login_url, login_data, format='json')

        # Verificamos que la respuesta sea 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verificamos que la respuesta contenga los tokens de acceso y el mensaje de éxito
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['message'], "Inicio de sesión exitoso")

    def test_inicio_sesion_credenciales_incorrectas(self):
        """
        Verifica que el sistema devuelve un error con credenciales incorrectas.
        Esto prueba un "flujo alternativo" del Caso de Uso CU-02.
        """
        # Creamos el usuario
        self.client.post(self.register_url, self.valid_user_data, format='json')

        invalid_login_data = {
            'username': 'testuser',
            'password': 'WrongPassword'
        }
        response = self.client.post(self.login_url, invalid_login_data, format='json')

        # Verificamos que la respuesta sea un error 401 (Unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Verificamos el mensaje de error personalizado
        self.assertEqual(response.data['detail'], "Usuario y Contraseña incorrecto")
