from django.test import TestCase
from django.contrib.auth import get_user_model

from django.contrib.auth.models import Permission

# Create your tests here.

Usuario = get_user_model()

class UserTestCase(TestCase):
    """
    Clase de prueba para el Modelo de Usuario.
    Hereda de TestCase, lo que significa que cada prueba se ejecutará en una base
    de datos temporal que se destruye automáticamente al finalizar.
    """

    def setUp(self):
        """
        El método setUp se ejecuta ANTES de cada prueba individual.
        Lo usamos para preparar los datos iniciales. Aquí creamos un usuario
        de prueba para no tener que crearlo repetidamente en cada test.
        """
        self.user = Usuario.objects.create_user(
            username='testuser',
            password='12345'
        )

    def test_user_creation_and_default_values(self):
        """
        Prueba que el usuario se crea correctamente y verifica los valores por defecto.
        - assertEqual: Verifica que dos valores sean idénticos.
        - assertTrue/assertFalse: Verifica que un valor sea verdadero o falso.
        """
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('12345'))
        # Verificar campos booleanos por defecto según nuestro modelo personalizado
        self.assertTrue(self.user.es_cliente)
        self.assertFalse(self.user.es_admin)

    def test_user_model_str(self):
        """
        Prueba el método __str__ del modelo de usuario.
        Asegura que cuando imprimimos el objeto usuario, nos devuelva su nombre (username).
        """
        self.assertEqual(str(self.user), 'testuser')

    def test_successful_login(self):
        """
        Prueba de 'camino feliz' (happy path) para el inicio de sesión.
        Utiliza el cliente de pruebas de Django (self.client) para simular
        el login de un usuario con las credenciales correctas.
        """
        login = self.client.login(username='testuser', password='12345')
        self.assertTrue(login)

    def test_failed_login(self):
        """
        Prueba de caso negativo (sad path).
        Simula un intento de login con una contraseña incorrecta y
        verifica que el sistema rechace el acceso (devuelva False).
        """
        login = self.client.login(username='testuser', password='wrongpassword')
        self.assertFalse(login)

    def test_nonexistent_user_login(self):
        """
        Prueba de caso negativo.
        Simula un intento de login de un usuario que no existe en la base de datos temporal
        y verifica que sea rechazado.
        """
        login = self.client.login(username='fantasma', password='12345')
        self.assertFalse(login)


class ViewsTestCase(TestCase):
    """
    Clase de prueba para las Vistas (Views) de la aplicación.
    Verifica que las rutas HTTP funcionen correctamente y respeten los permisos.
    """

    def setUp(self):
        """
        Prepara los datos antes de cada prueba de vista.
        Crea un usuario normal y un usuario administrador, asignándole a este último
        un permiso específico para poder probar las restricciones.
        """
        self.user = Usuario.objects.create_user(
            username='testuser',
            password='12345'
        )
        self.admin_user = Usuario.objects.create_user(
            username='adminuser',
            password='adminpassword'
        )
        # Asignamos el permiso explícito 'view_usuario' al administrador
        permission = Permission.objects.get(codename='view_usuario')
        self.admin_user.user_permissions.add(permission)

    def test_profile_unauthenticated(self):
        """
        Prueba que un usuario visitante (sin sesión) no pueda acceder a /perfil/.
        Debe recibir un código 302, lo que indica que Django lo está redirigiendo
        a la página de inicio de sesión de forma segura.
        """
        response = self.client.get('/perfil/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_profile_authenticated(self):
        """
        Prueba que un usuario que sí inició sesión pueda ver sus datos en /perfil/.
        Debe recibir un código HTTP 200 (OK) y los datos en formato JSON.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/perfil/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "usuario": "testuser",
            "email": ""
        })

    def test_admin_only_without_permission(self):
        """
        Prueba la seguridad basada en permisos.
        Un usuario normal (sin el permiso view_usuario) intenta acceder a /admin-only/.
        El servidor debe rechazar la solicitud con un código HTTP 403 (Prohibido).
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/admin-only/')
        self.assertEqual(response.status_code, 403)

    def test_admin_only_with_permission(self):
        """
        Prueba la seguridad basada en permisos.
        El usuario administrador (que sí tiene el permiso) intenta acceder a /admin-only/.
        El servidor debe darle acceso con un código HTTP 200 (OK).
        """
        self.client.login(username='adminuser', password='adminpassword')
        response = self.client.get('/admin-only/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"mensaje": "Acceso permitido solo a admins"})