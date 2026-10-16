from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from control_points.models import ControlPoint, TipoDato


class Elemento(models.Model):
    """
    Lo que se mide a lo largo del tiempo: una cámara, un vehículo, una sala...
    En la captura de "Reportes de Temperatura" de Qualitus estos aparecían
    agrupados por categoría (p. ej. "Cámaras de Obrador") y luego listados
    por nombre/matrícula individual.
    """

    nombre = models.CharField(max_length=120)
    categoria = models.CharField(
        max_length=120,
        help_text='Agrupación del elemento, p. ej. "Cámaras de Obrador", '
        '"Vehículos de Reparto".',
    )
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "elemento"
        ordering = ["categoria", "nombre"]
        constraints = [
            models.UniqueConstraint(
                fields=["categoria", "nombre"], name="unique_elemento_per_categoria"
            )
        ]

    def __str__(self) -> str:
        return f"{self.categoria} · {self.nombre}"


class Lectura(models.Model):
    """
    Una medición real, tomada en una fecha, de un punto de control sobre un
    elemento concreto. Esto es lo que en Qualitus se veía como "Reporte de
    Temperatura", "Reporte de Agua", etc. — todos son, en el fondo, lecturas
    contra un punto de control (ver analysis/qualitus-webapp/README.md).

    Solo uno de los tres campos de valor se usa, según
    `control_point.tipo_dato` — se valida en `clean()`.
    """

    control_point = models.ForeignKey(
        ControlPoint, on_delete=models.PROTECT, related_name="lecturas"
    )
    elemento = models.ForeignKey(Elemento, on_delete=models.PROTECT, related_name="lecturas")
    fecha = models.DateField()

    valor_numerico = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    valor_booleano = models.BooleanField(null=True, blank=True)
    valor_texto = models.TextField(blank=True)

    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="lecturas_registradas"
    )
    comentarios = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "lectura"
        ordering = ["-fecha", "elemento__categoria", "elemento__nombre"]
        constraints = [
            models.UniqueConstraint(
                fields=["control_point", "elemento", "fecha"],
                name="unique_lectura_per_control_point_elemento_fecha",
            )
        ]

    def __str__(self) -> str:
        return f"{self.elemento} · {self.control_point.nombre} · {self.fecha}"

    def clean(self):
        errors = {}
        tipo = self.control_point.tipo_dato if self.control_point_id else None

        valores_presentes = [
            nombre
            for nombre, valor in (
                ("valor_numerico", self.valor_numerico),
                ("valor_booleano", self.valor_booleano),
                ("valor_texto", self.valor_texto),
            )
            if valor not in (None, "")
        ]

        esperado = {
            TipoDato.NUMERICO: "valor_numerico",
            TipoDato.CHECKBOX: "valor_booleano",
            TipoDato.TEXTO: "valor_texto",
        }.get(tipo)

        if esperado and valores_presentes != [esperado]:
            errors["__all__"] = (
                f"Este punto de control es de tipo «{tipo}»: la lectura debe "
                f"traer únicamente el campo «{esperado}»."
            )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def dentro_de_rango(self) -> bool | None:
        """
        None cuando no aplica (punto de control no numérico, o rango sin
        definir). True/False cuando sí se puede evaluar — esto es lo que,
        más adelante, debería disparar una No Conformidad automática cuando
        sea False y el punto de control sea crítico.
        """
        if self.control_point.tipo_dato != TipoDato.NUMERICO or self.valor_numerico is None:
            return None
        minimo = self.control_point.valor_minimo_aceptable
        maximo = self.control_point.valor_maximo_aceptable
        if minimo is None or maximo is None:
            return None
        return Decimal(minimo) <= self.valor_numerico <= Decimal(maximo)
