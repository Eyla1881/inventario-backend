from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Usuario(AbstractUser):
    es_admin = models.BooleanField(default=False)
    es_cliente = models.BooleanField(default=True)

    def __str__(self):
        return self.username