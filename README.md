# Gestión de Usuarios e Inventario | User Management & Inventory System v1.0.0

🇺🇸 **English** | 🇪🇸 **Español**

---

## 🇺🇸 English

### Project Overview
This is a Django-based system designed to manage users with custom roles and an inventory of products. The project implements Role-Based Access Control (RBAC), ensuring that only authorized personnel can perform certain actions (like creating products).

### Features
- **Custom User Model**: Replaces Django's default user with a custom model that includes `es_admin` (is_admin) and `es_cliente` (is_client) roles.
- **Product Inventory**: A CRUD application for managing products.
- **Role-Based Access Control**:
  - Unauthenticated users are redirected to login.
  - Clients can view the product list.
  - Administrators can view and create new products.
- **Automated Testing & CI/CD**: Includes comprehensive unit tests and a GitHub Actions workflow to enforce code coverage.

### Prerequisites
Before you begin, ensure you have met the following requirements:
- **Python 3.11+** installed on your system.
- **Git** installed.
- **Pip** (Python package manager).

### Installation & Setup

1. **Clone the repository and enter the directory:**
   ```bash
   git clone <repository_url>
   cd gestion_de_usuarios
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   # source venv/bin/activate    # Mac/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional but recommended):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

### Test Users
To test the Role-Based Access Control, you can use the following credentials (or create your own):
- **Admin User:** `admin` / `admin` (Has `es_admin=True`, can access `/admin/` and create products).
- **Client User:** `cliente` / `cliente123` (Has `es_cliente=True`, restricted access).

### Running Tests
This project uses `coverage` to ensure all critical paths are tested.
```bash
coverage run manage.py test users products --verbosity=2
coverage report -m
```

---

## 🇪🇸 Español

### Descripción del Proyecto
Este es un sistema basado en Django diseñado para gestionar usuarios con roles personalizados y un inventario de productos. El proyecto implementa Control de Acceso Basado en Roles (RBAC), asegurando que solo el personal autorizado pueda realizar ciertas acciones (como crear productos).

### Características
- **Modelo de Usuario Personalizado**: Reemplaza el usuario por defecto de Django con un modelo que incluye los roles `es_admin` y `es_cliente`.
- **Inventario de Productos**: Una aplicación para gestionar productos.
- **Control de Acceso (Permisos)**:
  - Los visitantes sin sesión son redirigidos al login.
  - Los clientes pueden ver la lista de productos.
  - Los administradores pueden ver y crear nuevos productos.
- **Pruebas Automatizadas y CI/CD**: Incluye pruebas unitarias exhaustivas y un flujo de GitHub Actions para asegurar la cobertura del código.

### Requisitos Previos
Antes de comenzar, asegúrate de tener instaladas las siguientes herramientas:
- **Python 3.11+** instalado en tu sistema.
- **Git** instalado.
- **Pip** (Gestor de paquetes de Python).

### Instalación y Configuración

1. **Clonar el repositorio y entrar a la carpeta:**
   ```bash
   git clone <url_del_repositorio>
   cd gestion_de_usuarios
   ```

2. **Crear y activar un entorno virtual:**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   # source venv/bin/activate    # Mac/Linux
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Aplicar las migraciones de la base de datos:**
   ```bash
   python manage.py migrate
   ```

5. **Crear un superusuario (opcional pero recomendado):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Ejecutar el servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```

### Usuarios de Prueba
Para probar el Control de Acceso Basado en Roles, puedes usar las siguientes credenciales (o crear las tuyas propias):
- **Usuario Administrador:** `admin` / `admin` (Tiene `es_admin=True`, puede acceder a `/admin/` y crear productos).
- **Usuario Cliente:** `cliente` / `cliente123` (Tiene `es_cliente=True`, acceso restringido).

### Ejecución de Pruebas Unitarias
Este proyecto utiliza `coverage` para asegurar que todo el código importante esté cubierto por pruebas.
```bash
coverage run manage.py test users products --verbosity=2
coverage report -m
```

---

<!-- 
  =============================================================================
  SECCIÓN DIDÁCTICA: ¿CÓMO ESCRIBIR UN BUEN README?
  =============================================================================
-->

## 💡 Lección: ¿Cómo construir un README con Buenas Prácticas?

Un archivo `README.md` es la carta de presentación de tu código. Un buen proyecto con un mal README suele ser ignorado. Al crear el tuyo, asegúrate de seguir esta estructura de buenas prácticas:

1. **Título y Descripción Clara:** En los primeros 5 segundos, el lector debe saber qué hace el proyecto y para qué sirve. No asumas que saben de qué trata.
2. **Insignias (Badges):** (Opcional) Muestra si las pruebas pasan (como el check verde de GitHub Actions), la versión del código o la licencia.
3. **Requisitos Previos:** Enumera qué herramientas necesita tener instaladas el usuario antes de empezar (ej. Python 3.11, PostgreSQL, etc.).
4. **Instrucciones de Instalación:** Paso a paso literal. Desde cómo clonar el repositorio hasta cómo prender el servidor. Usa bloques de código `bash` para que el usuario solo tenga que hacer *copiar y pegar*.
5. **Uso o Características Clave:** Explica qué hace tu aplicación (ej. "Roles de Usuario", "Inventario CRUD").
6. **Pruebas (Testing):** Explica cómo correr las pruebas automáticas. Esto demuestra que tu código es profesional y confiable.
7. **Bilingüismo (Pro Tip):** Si buscas trabajo remoto o internacional, tener tu README en Inglés y Español te sumará muchísimos puntos frente a los reclutadores.
