FROM python:3.12-slim

# Evitar la creacin de archivos .pyc y forzar stdout
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

EXPOSE 8000

# Usamos python en vez de gunicorn por simplicidad en desarrollo
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
