from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Usuario propio desde el día uno (settings.AUTH_USER_MODEL), para no quedar
    atados al modelo por defecto de Django si más adelante hace falta algo
    específico del dominio (p. ej. vincular un usuario a un empleado de SAP,
    o a una categoría de permisos como el árbol de Qualitus actual).

    Por ahora no añade campos; está aquí para dejar la puerta abierta sin
    tener que migrar un modelo de usuario ya en producción.
    """

    class Meta:
        db_table = "accounts_user"
