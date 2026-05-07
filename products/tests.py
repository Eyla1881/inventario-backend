from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
import json
from .models import Product

Usuario = get_user_model()

class ProductModelTest(TestCase):
    """
    Clase de prueba para el modelo Product.
    Verifica si los objetos se crean correctamente en la base de datos temporal.
    """

    def test_product_creation(self):
        """
        Crea un producto y verifica que sus campos se hayan guardado correctamente.
        """
        product = Product.objects.create(
            name="Laptop",
            price=999.99,
            stock=10
        )
        self.assertEqual(product.name, "Laptop")
        self.assertEqual(product.price, 999.99)
        self.assertEqual(product.stock, 10)
        self.assertEqual(str(product), "Laptop")

class ProductViewsTest(TestCase):
    """
    Clase de prueba para las vistas de Product.
    Se enfoca fuertemente en el control de acceso (Autorización).
    """

    def setUp(self):
        """
        La configuración inicial (setUp) crea dos usuarios: un cliente normal y un admin.
        También crea un producto de prueba inicial para probar la vista de listado.
        """
        # Usuario cliente normal
        self.client_user = Usuario.objects.create_user(
            username='client',
            password='password123',
            es_cliente=True,
            es_admin=False
        )
        
        # Usuario administrador
        self.admin_user = Usuario.objects.create_user(
            username='admin',
            password='password123',
            es_cliente=False,
            es_admin=True
        )

        # Producto inicial de prueba
        self.product = Product.objects.create(name="Mouse", price=25.50, stock=50)

    def test_product_list_authenticated(self):
        """
        Prueba que cualquier usuario autenticado (ya sea cliente o admin) pueda ver la lista de productos.
        """
        # Iniciamos sesión como un cliente normal
        self.client.login(username='client', password='password123')
        
        # Hacemos una petición GET a la URL de la lista de productos
        response = self.client.get('/products/')
        
        # Esperamos un código de estado 200 OK (Éxito)
        self.assertEqual(response.status_code, 200)
        
        # Esperamos que la respuesta contenga nuestro producto de prueba
        data = response.json()
        self.assertIn("products", data)
        self.assertEqual(len(data["products"]), 1)
        self.assertEqual(data["products"][0]["name"], "Mouse")

    def test_product_list_unauthenticated(self):
        """
        Prueba que los usuarios NO autenticados sean redirigidos a la página de inicio de sesión
        cuando intentan ver los productos.
        """
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 302) # 302 es el código HTTP para Redirección

    def test_create_product_as_admin(self):
        """
        CAMINO FELIZ (Happy Path): Prueba que un administrador SÍ pueda crear un nuevo producto.
        """
        # Iniciamos sesión como administrador
        self.client.login(username='admin', password='password123')
        
        # Datos a enviar en la petición POST
        payload = {
            "name": "Keyboard",
            "price": 45.00,
            "stock": 20
        }
        
        # Hacemos la petición POST
        response = self.client.post('/products/create/', data=json.dumps(payload), content_type="application/json")
        
        # Esperamos un estado 201 Created (Creado)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 2) # Mouse + Keyboard

    def test_create_product_as_client_forbidden(self):
        """
        CAMINO TRISTE (Sad Path / Seguridad): Prueba que un cliente normal NO pueda crear un producto.
        Debería recibir una redirección 302 al login o un 403 Forbidden.
        (El decorador @user_passes_test de Django redirige al login por defecto si falla la validación).
        """
        # Iniciamos sesión como cliente
        self.client.login(username='client', password='password123')
        
        payload = {
            "name": "Hacker Item",
            "price": 0.00,
            "stock": 999
        }
        
        response = self.client.post('/products/create/', data=json.dumps(payload), content_type="application/json")
        
        # El cliente debe ser redirigido (302) a la página de login porque no pasa la prueba de seguridad (es_admin).
        self.assertEqual(response.status_code, 302)
        # Verificamos que no se haya creado ningún producto nuevo en la base de datos
        self.assertEqual(Product.objects.count(), 1)
