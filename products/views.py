from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Product
import json

def api_login_required(view_func):
    """
    Decorador API: Verifica si hay sesión iniciada.
    Si no, devuelve 401 Unauthorized en JSON.
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        return JsonResponse({"error": "No autorizado. Inicie sesión."}, status=401)
    return wrapper

def api_admin_required(view_func):
    """
    Decorador API: Verifica si el usuario es administrador.
    Si no, devuelve 403 Forbidden en JSON.
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and getattr(request.user, 'es_admin', False):
            return view_func(request, *args, **kwargs)
        return JsonResponse({"error": "Prohibido. Se requieren permisos de administrador."}, status=403)
    return wrapper

@api_login_required
def product_list(request):
    """
    Vista de Lectura (Read) para APIs.
    Devuelve todos los productos de la base de datos en formato JSON, 
    incluyendo la URL de la imagen si existe.
    """
    products = Product.objects.all()
    data = []
    for p in products:
        image_url = request.build_absolute_uri(p.image.url) if p.image else None
        data.append({
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": str(p.price),
            "stock": p.stock,
            "image": image_url
        })
    return JsonResponse({"products": data})

@csrf_exempt
@require_POST
@api_admin_required
def create_product(request):
    """
    Vista de Creación (Create) para APIs.
    Solo administradores pueden crear. Retorna 201 Created o 400 Bad Request.
    """
    try:
        data = json.loads(request.body)
        product = Product.objects.create(
            name=data.get('name'),
            description=data.get('description', ''),
            price=data.get('price', 0.0),
            stock=data.get('stock', 0)
        )
        return JsonResponse({"message": "Product created successfully", "id": product.id}, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
