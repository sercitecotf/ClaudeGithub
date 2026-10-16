from django.core.exceptions import ValidationError
from django.db import models


class TipoDato(models.TextChoices):
    NUMERICO = "numerico", "Numérico"
    CHECKBOX = "checkbox", "Checkbox"
    TEXTO = "texto", "Texto"


class Categoria(models.Model):
    """
    Agrupa puntos de control (p. ej. "Agua", "Limpieza"). En Qualitus esto
    aparecía como texto libre repetido por fila; aquí es su propia tabla
    para que no se puedan escribir variantes del mismo nombre por error
    ("Agua" / "agua " / "AGUA").
    """

    nombre = models.CharField(max_length=120, unique=True)

    class Meta:
        verbose_name = "categoría"
        verbose_name_plural = "categorías"
        ordering = ["nombre"]

    def __str__(self) -> str:
        return self.nombre


class ControlPoint(models.Model):
    """
    Un punto de control: qué se mide, en qué objeto/ubicación, con qué tipo
    de dato y qué rango se considera aceptable.

    Este modelo es el núcleo del sistema APPCC/HACCP: los reportes de
    Temperatura, Agua, Limpieza, etc. son, en el fondo, lecturas contra
    puntos de control definidos aquí (ver analysis/qualitus-webapp/README.md,
    sección "Puntos de Control").
    """

    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, related_name="puntos_de_control"
    )
    objeto = models.CharField(
        "objeto",
        max_length=200,
        help_text="Ubicación o equipo sobre el que se mide, p. ej. "
        "«Obrador frío lavamanos 1 (ALM 1)».",
    )
    nombre = models.CharField(
        "nombre",
        max_length=200,
        help_text="Qué se mide, p. ej. «Nivel de cloro libre», «Color».",
    )
    tipo_dato = models.CharField(max_length=20, choices=TipoDato.choices)

    valor_por_defecto = models.CharField(
        "valor por defecto",
        max_length=50,
        blank=True,
        help_text="Se interpreta según el tipo de dato: 'si'/'no' para "
        "checkbox, un número para numérico, texto libre para texto.",
    )
    valor_minimo_aceptable = models.DecimalField(
        "valor mínimo aceptable", max_digits=10, decimal_places=3, null=True, blank=True
    )
    valor_maximo_aceptable = models.DecimalField(
        "valor máximo aceptable", max_digits=10, decimal_places=3, null=True, blank=True
    )
    texto_por_defecto = models.TextField("texto por defecto", blank=True)
    unidad_medida = models.CharField("unidad de medida", max_length=30, blank=True)

    requisito = models.BooleanField(
        "requisito",
        default=False,
        help_text="Si está marcado, el punto de control proviene de un "
        "requisito normativo/contractual concreto (auditoría, certificación).",
    )
    critico = models.BooleanField(
        "crítico",
        default=False,
        help_text="Punto crítico de control (PCC) en el sentido APPCC/HACCP: "
        "un incumplimiento aquí dispara una no conformidad automáticamente.",
    )

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "punto de control"
        verbose_name_plural = "puntos de control"
        ordering = ["categoria__nombre", "objeto", "nombre"]
        constraints = [
            models.UniqueConstraint(
                fields=["categoria", "objeto", "nombre"],
                name="unique_control_point_per_object",
            )
        ]

    def __str__(self) -> str:
        return f"{self.objeto} · {self.nombre}"

    def clean(self):
        errors = {}

        if self.tipo_dato == TipoDato.NUMERICO:
            if self.valor_minimo_aceptable is None or self.valor_maximo_aceptable is None:
                errors["valor_minimo_aceptable"] = (
                    "Un punto de control numérico necesita valor mínimo y "
                    "máximo aceptable."
                )
            elif self.valor_minimo_aceptable > self.valor_maximo_aceptable:
                errors["valor_minimo_aceptable"] = (
                    "El valor mínimo aceptable no puede ser mayor que el máximo."
                )
            if not self.unidad_medida:
                errors["unidad_medida"] = (
                    "Un punto de control numérico necesita unidad de medida."
                )
        else:
            # Checkbox y texto no usan rango numérico: si se definieron por
            # error (p. ej. al cambiar el tipo de dato de un punto existente)
            # se limpian para que no queden datos contradictorios en la fila.
            if self.valor_minimo_aceptable is not None or self.valor_maximo_aceptable is not None:
                errors["tipo_dato"] = (
                    "Solo un punto de control numérico puede tener valor "
                    "mínimo/máximo aceptable."
                )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
