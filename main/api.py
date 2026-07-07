from ninja import NinjaAPI
from products.api import router as products_router
from users.api import router as users_router

api = NinjaAPI(
    title="API del Proyecto",
    description="Documentacin interactiva con Swagger generada por django-ninja (estilo FastAPI)",
    version="1.0.0"
)

api.add_router("/products/", products_router)
api.add_router("/users/", users_router)
