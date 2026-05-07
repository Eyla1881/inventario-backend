from django.db import models

class Product(models.Model):
    """
    Modelo de Base de Datos para los Productos.
    Heredar de models.Model convierte esta clase en una tabla de base de datos.
    Cada atributo será una columna en la tabla.
    """
    # CharField es para textos cortos (como VARCHAR en SQL)
    name = models.CharField(max_length=100, verbose_name="Nombre")
    
    # TextField es para textos largos sin límite definido. 
    # blank=True y null=True permiten que este campo sea opcional.
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")
    
    # DecimalField se usa para dinero, evitando los errores de redondeo de los FloatField.
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    
    # IntegerField para números enteros (no puedes tener medio producto en stock).
    stock = models.IntegerField(default=0, verbose_name="Stock Disponible")

    # ImageField para la foto del producto. Requiere Pillow.
    image = models.ImageField(upload_to='product_images/', blank=True, null=True, verbose_name="Imagen")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        """
        Método mágico de Python que define cómo se muestra este objeto en texto.
        Por ejemplo, en el panel de administrador, en lugar de ver "Product Object(1)",
        veremos el nombre del producto (ej: "Laptop").
        """
        return self.name
