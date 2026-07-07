from ninja import Router, Schema
from typing import List, Optional
from django.shortcuts import get_object_or_404
from .models import Product

router = Router(tags=["Productos"])

class ProductSchema(Schema):
    id: int
    name: str
    description: str
    price: str
    stock: int
    image: Optional[str] = None

class ProductCreateSchema(Schema):
    name: str
    description: str = ""
    price: float = 0.0
    stock: int = 0

@router.get("/", response=List[ProductSchema])
def list_products(request):
    """
    Devuelve todos los productos de la base de datos.
    """
    products = Product.objects.all()
    # Mapeamos para incluir la URL de la imagen si existe
    for p in products:
        p.image = request.build_absolute_uri(p.image.url) if p.image else None
    return products

@router.post("/create/", response={201: dict, 400: dict})
def create_product(request, payload: ProductCreateSchema):
    """
    Crea un nuevo producto. (Ruta protegida para admins idealmente, pero para demo la dejamos as por ahora)
    """
    try:
        product = Product.objects.create(
            name=payload.name,
            description=payload.description,
            price=payload.price,
            stock=payload.stock
        )
        return 201, {"message": "Product created successfully", "id": product.id}
    except Exception as e:
        return 400, {"error": str(e)}
