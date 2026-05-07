from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import json

@login_required
def perfil(request):
    return JsonResponse({
        "usuario": request.user.username,
        "email": request.user.email
    })

@permission_required('users.view_usuario', raise_exception=True)
def solo_admin(request):
    return JsonResponse({"mensaje": "Acceso permitido solo a admins"})

@csrf_exempt
def api_login(request):
    """
    Endpoint para iniciar sesión desde un Frontend (React/Next.js).
    Recibe username y password en JSON y devuelve una cookie de sesión.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Verificar si el usuario es cliente
                if user.is_superuser or getattr(user, 'es_admin', False):
                    return JsonResponse({"error": "Los administradores deben ingresar por el panel de gestión (/admin)."}, status=403)
                
                login(request, user)
                return JsonResponse({
                    "message": "Login exitoso",
                    "user": {
                        "username": user.username,
                        "es_admin": False,
                        "es_cliente": True
                    }
                })
            else:
                return JsonResponse({"error": "Credenciales inválidas"}, status=401)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)

def api_logout(request):
    logout(request)
    return JsonResponse({"message": "Logout exitoso"})

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({"message": "CSRF cookie set"})