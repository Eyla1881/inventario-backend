from ninja import Router, Schema
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from typing import Optional

router = Router(tags=["Usuarios"])

class LoginSchema(Schema):
    username: str
    password: str

class UserSchema(Schema):
    username: str
    es_admin: bool
    es_cliente: bool

@router.get("/perfil/")
def perfil(request):
    if not request.user.is_authenticated:
        return 401, {"error": "No autorizado"}
    return {
        "usuario": request.user.username,
        "email": request.user.email
    }

@router.post("/login/", response={200: dict, 401: dict, 403: dict})
def api_login(request, payload: LoginSchema):
    """
    Endpoint para iniciar sesin.
    """
    user = authenticate(request, username=payload.username, password=payload.password)
    if user is not None:
        if user.is_superuser or getattr(user, 'es_admin', False):
            return 403, {"error": "Los administradores deben ingresar por el panel de gestin (/admin)."}
        
        login(request, user)
        return 200, {
            "message": "Login exitoso",
            "user": {
                "username": user.username,
                "es_admin": False,
                "es_cliente": True
            }
        }
    return 401, {"error": "Credenciales invlidas"}

@router.post("/logout/")
def api_logout(request):
    logout(request)
    return {"message": "Logout exitoso"}

@router.get("/csrf/")
def get_csrf_token(request):
    get_token(request) # Esto asegura que se establezca la cookie CSRF
    return {"message": "CSRF cookie set"}
